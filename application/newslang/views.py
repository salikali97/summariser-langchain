
from flask import jsonify, request
from application.constants import Methods, APIroutes
from . import newslang
from application.configuration import openai_key
from application import logger
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import openai
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain


@newslang.route("/", methods=[Methods.GET])
def base_url():
    """
    Base url GET API required for HTTPS conversion
    """
    response = {"response": "Valid Response"}
    logger.info(f"Response: {response}")
    return jsonify(response), 200


@newslang.route(APIroutes.NEWS_LANG, methods=[Methods.POST])
def newslang():
    try:
        """
            This function gets the summary of various news artcile
        """
        news = request.json

        prompt_template = """You are an expert news summarizer which summarizes news articles with accuracy, 
        given an input which has a titles,urls and contents,summarize the content of articles provided. 
        Each news summary with title and content MUST NOT be more than 400 words AND you must keep a check for duplicacy of 
        news and summarize only one of the articles if there is a duplicate present. You MUST give the response in the form
        'title' which is the title of the article, 'url' which is the url of the article 
        and 'content' which is the summarized content of the article, ALWAYS maintain the order of sending Title,URL,Content
        Write a concise summary of the following: `{text}` 
        CONSCISE SUMMARY OF EACH NEWS SEPARATELY IN ENGLISH:"""
        model_name = "gpt-3.5-turbo"

        # define the prompt template and llm models
        llm=ChatOpenAI(openai_api_key=openai_key,model_name = 'gpt-3.5-turbo')
        prompt = PromptTemplate(
            input_variables=['text'],
            template=prompt_template
        )
        
        # convert the text into document format
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            model_name=model_name
        )
        texts = text_splitter.split_text(news['news'])
        docs = [Document(page_content=t) for t in texts]
        logger.info(f"Length of docs: {len(docs)}")
        
        # restrict the tokens 
        num_tokens = llm.get_num_tokens(prompt_template)
        gpt_35_turbo_max_tokens = 2000
        verbose = True

        # initialize the summarize chain on the basis of number of tokens
        if num_tokens < gpt_35_turbo_max_tokens:
            chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
        else:
            chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=verbose)

        # run the chain
        summary = chain.run(docs)

        logger.info(f"Summary: {summary}")

        return jsonify(summary), 200
    except Exception as e:
        logger.info(e)
        return (jsonify([]))
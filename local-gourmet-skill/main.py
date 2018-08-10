# -*- coding: utf-8 -*-

import os
import logging

import boto3
from boto3.dynamodb.conditions import Key, Attr

from flask import (
    Flask, request, jsonify
)
from cek import (
    Clova, SpeechBuilder, ResponseBuilder
)

# flask
app = Flask(__name__)

# logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Clova
application_id = os.environ.get('CLOVA_APPLICATION_ID')
clova = Clova(
    application_id=application_id, 
    default_language='ja', 
    debug_mode=False)
speech_builder = SpeechBuilder(default_language='ja')
response_builder = ResponseBuilder(default_language='ja')

@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked index()')
    return 'hello from Flask!'

@app.route('/clova', methods=['POST'])
def clova_service():
    resp = clova.route(request.data, request.headers)
    resp = jsonify(resp)
    # make sure we have correct Content-Type that CEK expects
    resp.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return resp


'''
===================================
Clova RequestHandler 用メソッド
===================================
'''


@clova.handle.launch
def launch_request_handler(clova_request):
    text = 'ご当地グルメを調べたい都道府県名か、詳しく知りたいご当地グルメの名前を教えてください。'
    response = response_builder.simple_speech_text(text)
    response_builder.add_reprompt(response, text)
    return response


@clova.handle.default
def default_handler(clova_request):
    return clova.response('もう一度お願いします')


@clova.handle.intent('FindGourmetByPrefectureIntent')
def find_gourmet_by_prefecture_intent_handler(clova_request):
    '''
    都道府県に応じたご当地グルメ情報メッセージを返すインテント
    （FindGourmetByPrefectureIntent）判別時に呼ばれるメソッド

    Parameters
    ----------
    clova_request : Request
        Intent 判別時のリクエスト
    
    Returns
    -------
    builder : Response
        都道府県に応じたご当地グルメ情報メッセージを含めたResponse
    '''
    logger.info('find_gourmet_by_prefecture_intent_handler method called!!')
    prefecture = clova_request.slot_value('prefecture')
    logger.info('Prefecture: %s', prefecture)
    response = None
    if prefecture is not None:
        try:
            # 都道府県名を判別できた場合
            response = make_gourmet_info_message_by_prefecture(prefecture)
        except Exception as e:
            # 処理中に例外が発生した場合は、最初からやり直してもらう
            logger.error('Exception at make_gourmet_info_message_for: %s', e)
            text = '処理中にエラーが発生しました。もう一度はじめからお願いします。'
            response = response_builder.simple_speech_text(text)
    else:
        # 都道府県名を判別できなかった場合
        text = 'もう一度、ご当地グルメを調べたい都道府県名を教えてください。'
        response = response_builder.simple_speech_text(text)
        response_builder.add_reprompt(response, 
            'ご当地グルメを調べたい都道府県名を教えてください。')
    # retrun
    return response


@clova.handle.intent('FindGourmetByNameIntent')
def find_gourmet_by_name_intent_handler(clova_request):
    '''
    ご当地グルメ名に応じたご当地グルメ情報メッセージを返すインテント
    （FindGourmetByNameIntent）判別時に呼ばれるメソッド

    Parameters
    ----------
    clova_request : Request
        Intent 判別時のリクエスト
    
    Returns
    -------
    builder : Response
        ご当地グルメ名に応じたご当地グルメ情報メッセージを含めたResponse
    '''
    logger.info('find_gourmet_by_name_intent_handler method called!!')
    gourmet_name = clova_request.slot_value('gourmet')
    logger.info('Gourmet: %s', gourmet_name)
    response = None
    if gourmet_name is not None:
        try:
            # ご当地グルメ名を判別できた場合
            response = make_gourmet_info_message_by_name(gourmet_name)
        except Exception as e:
            # 処理中に例外が発生した場合は、最初からやり直してもらう
            logger.error('Exception at make_gourmet_info_message_for: %s', e)
            text = '処理中にエラーが発生しました。もう一度はじめからお願いします。'
            response = response_builder.simple_speech_text(text)
    else:
        # ご当地グルメ名を判別できなかった場合
        text = 'もう一度、調べたいご当地グルメの名前を教えてください。'
        response = response_builder.simple_speech_text(text)
        response_builder.add_reprompt(response, 
            'ご当地グルメの名前を教えてください。')
    # retrun
    return response


'''
===================================
Clova に返すResponse 生成用メソッド
===================================
'''


def make_gourmet_info_message_by_prefecture(prefecture):
    '''
    都道府県に応じたご当地グルメ情報メッセージを生成する

    Parameters
    ----------
    prefecture : str
        都道府県名
    
    Returns
    -------
    builder : Response
        都道府県に応じたご当地グルメ情報メッセージを含めたResponse
    '''
    logger.info('make_gourmet_info_message_by_prefecture method called!!')
    try:
        gourmet_info_list = inquiry_gourmet_info_list_for(prefecture)
        message = ''
        reprompt = None
        end_session = False
        if gourmet_info_list is None:
            # ご当地グルメ情報が登録されていない場合
            message = '{} にはご当地グルメ情報が登録されていませんでした。他の都道府県で試してください。'.format(
                prefecture
            )
            reprompt = 'ご当地グルメを調べたい都道府県名を教えてください。'
        elif len(gourmet_info_list) == 1:
            # ご当地グルメ情報が1件だけ登録されている場合
            gourmet_info = gourmet_info_list[0]
            gourmet_info_detail = gourmet_info['detail']
            if gourmet_info_detail.endswith('。') == False:
                gourmet_info_detail += 'です。'
            message = '{} のご当地グルメは {} です。{}'.format(
                prefecture,
                gourmet_info['yomi'],
                gourmet_info_detail
            )
            # ご当地グルメ情報を返してスキルのセッションを完了させる
            end_session = True
        else:
            # ご当地グルメ情報が複数件登録されている場合
            gourmet_names = ''
            for info in gourmet_info_list:
                gourmet_names += info['yomi'] + '、'
            message = '{} には、{} 件のご当地グルメが登録されています。'.format(
                prefecture,
                len(gourmet_info_list)
            )
            message += '詳しく知りたいご当地グルメがあればお調べしますので、ご当地グルメ名をお知らせください。'
            message += '登録されているご当地グルメは、{} です。'.format(gourmet_names)
        # build response
        response = response_builder.simple_speech_text(message, end_session=end_session)
        if reprompt is not None:
            response = response_builder.add_reprompt(response, reprompt)
        return response
    except Exception as e:
        logger.error('Exception at make_gourmet_info_message_by_prefecture: %s', e)
        raise e



def make_gourmet_info_message_by_name(gourmet_name):
    '''
    ご当地グルメ名に応じたメッセージを生成する

    Parameters
    ----------
    gourmet_name : str
        ご当地グルメ名
    
    Returns
    -------
    builder : Response
        ご当地グルメ名に応じたご当地グルメ情報メッセージを含めたResponse
    '''
    logger.info('make_gourmet_info_message_by_name method called!!')
    try:
        gourmet_info = get_gourmet_info_for(gourmet_name)
        message = ''
        reprompt = None
        end_session = False
        if gourmet_info is None:
            # ご当地グルメ情報が見つからない場合
            message = '{} という名前のご当地グルメ情報が見つかりませんでした。もう一度教えてください。'.format(
                gourmet_name
            )
            reprompt = '調べたいご当地グルメの名前を教えてください。'
        else:
            # ご当地グルメ情報が見つかった場合
            gourmet_info_detail = gourmet_info['detail']
            if gourmet_info_detail.endswith('。') == False:
                gourmet_info_detail += 'です。'
            message = '{} は、{} のご当地グルメです。{}'.format(
                gourmet_info['yomi'],
                gourmet_info['prefecture'],
                gourmet_info_detail
            )
            end_session = True
        # build response
        response = response_builder.simple_speech_text(message, end_session=end_session)
        if reprompt is not None:
            response = response_builder.add_reprompt(response, reprompt)
        return response
    except Exception as e:
        logger.error('Exception at make_gourmet_info_message_by_name: %s', e)
        raise e


'''
===================================
DynamoDB 関連メソッド
===================================
'''


def inquiry_gourmet_info_list_for(prefecture):
    '''
    都道府県に応じたご当地グルメ情報を取得する

    Parameters
    ----------
    prefecture : str
        都道府県名
    
    Returns
    -------
    gourmet_info_list : list
        都道府県に応じたご当地グルメ情報のリスト
    '''
    logger.info('inquiry_gourmet_info_list_for method called!!')
    if prefecture is None or '' == prefecture:
        raise ValueError('prefecture is None or empty...')
    # query
    try:
        endpoint_url = os.getenv('DYNAMODB_ENDPOINT', None)
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        table = dynamodb.Table(os.environ.get('TABLE_GOURMET_INFO', '') )
        response = table.scan(
            FilterExpression=Attr('prefecture').eq(prefecture)
        )
        gourmet_info_list = response.get('Items', None)
        if gourmet_info_list is None or len(gourmet_info_list) <= 0:
            gourmet_info_list = None
        return gourmet_info_list
    except Exception as e:
        logger.error('Exception at inquiry_gourmet_info_list_for: %s', e)
        raise e


def get_gourmet_info_for(gourmet_name):
    '''
    指定したご当地グルメ名の情報を取得する
    存在しない場合はNoneを返す。

    Parameters
    ----------
    gourmet_name : str
        ご当地グルメ名
    
    Returns
    -------
    gourmet_info : dict
        ご当地グルメ名に応じたご当地グルメ情報
    '''
    logger.info('get_gourmet_info_for method called!! [Gourmet:%s]', gourmet_name)
    logger.info('inquiry_gourmet_info_list_for method called!!')
    if gourmet_name is None or '' == gourmet_name:
        raise ValueError('gourmet_name is None or empty...')
    try:
        endpoint_url = os.getenv('DYNAMODB_ENDPOINT', None)
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        table = dynamodb.Table(os.environ.get('TABLE_GOURMET_INFO', '') )
        response = table.get_item(
            Key={
                'name': gourmet_name
            }
        )
        result = None
        item = response.get('Item', None)
        if item:
            result = item 
        return result
    except Exception as e:
        logger.error('Exception at get_gourmet_info_for: %s', e)
        raise e

if __name__ == '__main__':
    app.run(debug=True)

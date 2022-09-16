from flask import Flask

class BaseController:
    
        
    # Send Success Response
    def sendResponse(self,message,data={},fields={},status=200):
        response = {}
        response['success'] = True;
        response['message'] = message;
        response['data'] = data;
        response['fields'] = fields;
        response['status_code']  = status;

        return response;
    # Send Error Response
    def sendError(self,message,fields={},data={},status=400):
        response = {}
        response['success'] = False;
        response['message'] = message;
        response['data'] = data;
        response['fields'] = fields;
        response['status_code']  = status;

        return response;


        
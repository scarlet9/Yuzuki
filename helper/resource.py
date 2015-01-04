# -*- coding: utf-8 -*-
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from twisted.web.resource import Resource
from twisted.web.http import FORBIDDEN

from helper.md_ext import MarkdownExtension

class YuzukiResource(Resource):
    jinja2_ext = [
        MarkdownExtension,
    ]
    jinja2_env = Environment(loader=FileSystemLoader("template",
                                                     encoding="utf-8"),
                             extensions=jinja2_ext)
    jinja2_env.globals = {
        "datetime": datetime,
    }
    
    def render(self, request):
        request.initialize(self)
        request.logger.info(request.path + " " + request.getClientIP())
        # TODO: auto login
        result = Resource.render(self, request)
        request.finalize()
        result.encode("UTF-8")
        return result
    
    @staticmethod
    def get_template(name, parent=None, glob=None):
        return YuzukiResource.jinja2_env.get_template(name, parent, glob)
    
    @staticmethod
    def render_template(name, request, context=None):
        if context == None:
            context = dict()
        context["request"] = request
        return YuzukiResource.get_template(name).render(context).encode("utf-8")
    
    @staticmethod
    def render_template_from_text(text, context=None):
        if context == None:
            context = dict()
        template = YuzukiResource.jinja2_env.from_string(text)
        return template.render(context).encode("utf-8")
    
    @staticmethod
    def generate_error_message(request, code, brief, detail):
        context = {
            "brief"     : brief,
            "detail"    : detail,
            "title"     : str(code) + " - " + str(brief),
        }
        return YuzukiResource.render_template("error.html", request, context)

def need_login(f):
    def _render_wrapper(resource, request):
        if request.user:
            return f(resource, request)
        else:
            request.setResponseCode(FORBIDDEN)
            return YuzukiResource.generate_error_message(request,
                                                         FORBIDDEN,
                                                         "Forbidden",
                                                         "로그인 한 사용자만 볼 수 있는 페이지입니다")
    return _render_wrapper

def need_admin_permission(f):
    def _render_wrapper(resource, request):
        if request.user and request.user.is_admin:
            return f(resource, request)
        else:
            request.setResponseCode(FORBIDDEN)
            return YuzukiResource.generate_error_message(request,
                                                         FORBIDDEN,
                                                         "Forbidden",
                                                         "관리자만 볼 수 있는 페이지입니다")
    return _render_wrapper
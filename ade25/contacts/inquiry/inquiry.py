# -*- coding: utf-8 -*-
"""Module providing inquiry form processing"""
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter

from ade25.contacts.inquiry.mailer import create_plaintext_message
from ade25.contacts.inquiry.mailer import prepare_email_message
from ade25.contacts.inquiry.mailer import get_mail_template
from ade25.contacts.inquiry.mailer import send_mail

from ade25.contacts import _


class InquiryFormView(BrowserView):
    """ Inquiry form """

    def __call__(self):
        self.errors = {}
        return self.render()

    def update(self):
        translation_service = api.get_tool(name="translation_service")
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('email', 'subject')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error_msg = _(u"This field is required")
                        error['active'] = True
                        error['msg'] = translation_service.translate(
                            error_msg,
                            'ade25.contacts',
                            target_language=api.portal.get_default_language()
                        )
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self.send_inquiry(form)

    def render(self):
        self.update()
        return self.index()

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value

    def send_inquiry(self, data):
        translation_service = api.get_tool(name="translation_service")
        context = aq_inner(self.context)
        subject = _(u"Inquiry from website visitor")
        mail_tpl = self._compose_message(data)
        mail_plain = create_plaintext_message(mail_tpl)
        msg = prepare_email_message(mail_tpl, mail_plain)
        default_email = api.portal.get_registry_record('plone.email_from_address')
        recipient_email = getattr(context, 'email', default_email)
        recipients = [recipient_email,
                      'info@kreativkombinat.de']
        send_mail(
            msg,
            recipients,
            translation_service.utranslate(
                subject,
                'ade25.contacts',
                target_language=api.portal.get_default_language()
            )
        )
        next_url = context.absolute_url()
        msg = _(u"Thank you for your interest. Your message has been sent.")
        api.portal.show_message(message=msg, request=self.request)
        return self.request.response.redirect(next_url)

    def _compose_message(self, data):
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        template_vars = {
            'email': data['email'],
            'subject': str(data['subject']),
            'message': data['comment'],
            'url': portal_url
        }
        template_name = 'inquiry-mail.html'
        message = get_mail_template(template_name, template_vars)
        return message


class InquiryFormEmail(BrowserView):
    """ Embeddable email field """

    def __call__(self):
        self.errors = {}
        return self.render()

    def render(self):
        return self.index()

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value


class InquiryFormSubject(BrowserView):
    """ Embeddable email field """

    def __call__(self):
        self.errors = {}
        return self.render()

    def render(self):
        return self.index()

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value


class InquiryFormCommentView(BrowserView):
    """ Embeddable comment textarea """

    def __call__(self):
        self.errors = {}
        return self.render()

    def render(self):
        return self.index()

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value

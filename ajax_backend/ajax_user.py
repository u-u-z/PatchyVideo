
import time

import redis

from flask import render_template, request, current_app, jsonify, redirect, session

from init import app
from utils.interceptors import loginOptional, jsonRequest, basePage, loginRequiredJSON
from utils.jsontools import *

from spiders import dispatch

from services.user import *
from config import UserConfig

@app.route('/auth/get_session.do', methods = ['POST'])
@basePage
@jsonRequest
def ajax_auth_get_session_do(rd, data):
	ret = require_session(data.type)
	return "json", makeResponseSuccess(ret)

@app.route('/login.do', methods = ['POST'])
@basePage
@jsonRequest
def ajax_login(rd, data):
	sid = login(data.username, data.password, '', data.session)
	session['sid'] = sid

@app.route('/signup.do', methods = ['POST'])
@basePage
@jsonRequest
def ajax_signup(rd, data):
	uid = signup(data.username, data.password, data.email, '', data.session)
	return "json", makeResponseSuccess({'uid': str(uid)})

@app.route('/user/changedesc.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_changedesc(rd, user, data):
	update_desc(session['sid'], user['_id'], data.desc)

@app.route('/user/changepass.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_changepass(rd, user, data):
	update_password(user['_id'], data.old_pass, data.new_pass)

@app.route('/user/admin/updaterole.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_updaterole(rd, user, data):
	updateUserRole(user['_id'], data.role, user)

@app.route('/user/admin/updatemode.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_updatemode(rd, user, data):
	updateUserAccessMode(user['_id'], data.mode, user)

@app.route('/user/admin/get_allowedops.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_get_allowedops(rd, user, data):
	ret = getUserAllowedOps(user['_id'], user)
	return "json", makeResponseSuccess(ret)

@app.route('/user/admin/get_deniedops.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_get_get_deniedops(rd, user, data):
	ret = getUserDeniedOps(user['_id'], user)
	return "json", makeResponseSuccess(ret)

@app.route('/user/admin/update_allowedops.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_update_allowedops(rd, user, data):
	updateUserAllowedOps(user['_id'], data.ops, user)

@app.route('/user/admin/update_deniedops.do', methods = ['POST'])
@loginRequiredJSON
@jsonRequest
def ajax_user_update_deniedops(rd, user, data):
	updateUserDeniedOps(user['_id'], data.ops, user)

from rest.rest_base import HttpClient
import common.utility as util
import json


class CloudPlatformService(HttpClient):
    def __init__(self):
        super().__init__()
        self.default_genesis_url = super().default_genesis_url
        self.default_cloud_platform_url = super().default_cloud_platform_url
        self.default_headers = {'Content-Type': 'application/json'}

    @staticmethod
    def set_request_header(x_t, x_sn, x_st):
        return {
            'Content-Type': 'application/json',
            'X-T': str(x_t),
            'X-SN': x_sn,
            'X-ST': x_st
        }

    # The following APIs are about users
    def user_login(self, req_body):
        api_url = '/api/login'
        url = self.default_cloud_platform_url + api_url
        login_response = super().send_requests_without_cookie('POST', url, req_body=req_body,
                                                              req_headers=self.default_headers)
        return login_response.cookies

    def user_login_response(self, req_body):
        api_url = '/api/login'
        url = self.default_cloud_platform_url + api_url
        login_response = super().send_requests_without_cookie('POST', url, req_body=req_body,
                                                              req_headers=self.default_headers)
        return login_response.json()

    def user_logout(self, cookies):
        api_url = '/api/logout'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        logout_response = super().send_requests('GET', url, req_body=None, req_headers=user_headers,
                                                req_cookies=cookies)
        return logout_response

    def user_get_verify_code(self, cookies):
        api_url = '/api/verifyCode'
        url = self.default_cloud_platform_url + api_url

        get_code_response = super().send_requests('GET', url, req_body=None, req_headers=self.default_headers,
                                                  req_cookies=cookies)
        return get_code_response

    def user_get_password_public_key(self):
        api_url = '/api/passPublicKey'
        url = self.default_cloud_platform_url + api_url

        get_public_key_response = super().send_requests('GET', url, req_body=None, req_headers=self.default_headers,
                                                        req_cookies=None)
        return get_public_key_response.json()['body']['key']

    def get_dynamic_salt(self, cookies):
        api_url = '/api/dynamicSalt'
        url = self.default_cloud_platform_url + api_url

        salt_response = super().send_requests('GET', url, req_body=None, req_headers=self.default_headers,
                                              req_cookies=cookies)
        return salt_response.json()['body']['salt']

    def user_send_reset_email(self, req_body, cookies):
        api_url = '/api/user-e/send-reset-email'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        reset_email_response = super().send_requests('POST', url, req_body=req_body, req_headers=user_headers,
                                                     req_cookies=cookies)
        return reset_email_response

    def user_forget_password(self, req_body, cookies):
        api_url = '/api/user-e/reset-password'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        reset_password_response = super().send_requests('POST', url, req_body=req_body, req_headers=user_headers,
                                                        req_cookies=cookies)
        return reset_password_response

    def create_user(self, req_body, cookies):
        api_url = '/api/user'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        add_user_response = super().send_requests('PUT', url, req_body=req_body, req_headers=user_headers,
                                                  req_cookies=cookies)
        return add_user_response.json()

    def delete_user_by_id(self, user_id, cookies):
        api_url = '/api/user/' + user_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        delete_user_response = super().send_requests('DELETE', url, req_body=None, req_headers=user_headers,
                                                     req_cookies=cookies)
        return delete_user_response.json()

    def update_user_info(self, req_body, user_id, cookies):
        api_url = '/api/user/' + user_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        update_user_response = super().send_requests('POST', url, req_body=req_body, req_headers=user_headers,
                                                     req_cookies=cookies)
        return update_user_response.json()

    def get_single_user_info_by_id(self, user_id, cookies):
        api_url = '/api/user/' + user_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        user_response = super().send_requests('GET', url, req_body=None, req_headers=user_headers, req_cookies=cookies)
        return user_response.json()

    def get_single_user_info_by_account(self, account_name, cookies):
        api_url = '/api/user-e/account/' + account_name
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        user_response = super().send_requests('GET', url, req_body=None, req_headers=user_headers, req_cookies=cookies)
        return user_response.json()['body']

    def search_users(self, search_user_query, page, page_size, cookies):
        api_url = '/api/users'
        query_url = ''
        if search_user_query['account'] is not None:
            query_url = 'account=' + search_user_query['account']
        if search_user_query['orgId'] is not None:
            query_url = 'orgId=' + search_user_query['orgId']
        if search_user_query['role'] is not None:
            query_url = 'role=' + search_user_query['role']
        if search_user_query['status'] is not None:
            query_url = 'status=' + search_user_query['status']
        if search_user_query['accountType'] is not None:
            query_url = 'accountType=' + search_user_query['accountType']
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        user_response = super().send_requests('GET', url, req_body=None, req_headers=user_headers, req_cookies=cookies)
        return user_response.json()['body']

    def user_change_role(self, user_id, req_body, cookies):
        api_url = '/api/user/' + user_id + '/change-role'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        user_response = super().send_requests('POST', url, req_body=req_body, req_headers=user_headers,
                                              req_cookies=cookies)
        return user_response.json()

    def user_bind_unity_account(self, req_body, cookies):
        api_url = '/api/user-e/bind-account'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        user_response = super().send_requests('POST', url, req_body=req_body, req_headers=user_headers,
                                              req_cookies=cookies)
        return user_response.json()

    def user_reset_password(self, user_id, req_body, cookies):
        api_url = '/api/user/' + user_id + '/reset-password'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        user_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        user_response = super().send_requests('POST', url, req_body=req_body, req_headers=user_headers,
                                              req_cookies=cookies)
        return user_response.json()

    def user_change_org(self, user_id, org_id, cookies):
        api_url = '/api/user/' + user_id + '/change-org/' + org_id

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        url = self.default_cloud_platform_url + api_url
        user_response = super().send_requests('GET', url, req_body=None, req_headers=org_headers, req_cookies=cookies)
        return user_response.json()

    # The following APIs are about organizations
    def create_organization(self, req_body, cookies):
        api_url = '/api/org'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        organization_response = super().send_requests('PUT', url, req_body=req_body, req_headers=org_headers,
                                                      req_cookies=cookies)
        return organization_response.json()

    def search_organization(self, org_name, page, page_size, cookies):
        api_url = '/api/orgs'
        query_url = ''
        if org_name is not None:
            query_url = 'name=' + org_name
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        organization_response = super().send_requests('GET', url, req_body=None, req_headers=org_headers,
                                                      req_cookies=cookies)
        return organization_response.json()['body']

    def get_organization_by_id(self, org_id, cookies):
        api_url = '/api/org/' + org_id

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        url = self.default_cloud_platform_url + api_url
        organization_response = super().send_requests('GET', url, req_body=None, req_headers=org_headers,
                                                      req_cookies=cookies)
        return organization_response.json()['body']

    def update_organization(self, org_id, req_body, cookies):
        api_url = '/api/org/' + org_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        organization_response = super().send_requests('POST', url, req_body=req_body, req_headers=org_headers,
                                                      req_cookies=cookies)
        return organization_response.json()['body']

    def delete_organization_by_id(self, org_id, cookies):
        api_url = '/api/org/' + org_id

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        url = self.default_cloud_platform_url + api_url
        organization_response = super().send_requests('DELETE', url, req_body=None, req_headers=org_headers,
                                                      req_cookies=cookies)
        return organization_response.json()['body']

    def bind_organization(self, req_body, cookies):
        api_url = '/api/org-e/relate-org'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        org_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        organization_response = super().send_requests('POST', url, req_body=req_body, req_headers=org_headers,
                                                      req_cookies=cookies)
        return organization_response.json()

    # The following APIs are about projects
    def create_project(self, org_id, req_body, cookies):
        api_url = '/api/organizations/' + org_id + '/projects'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        project_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        project_response = super().send_requests('POST', url, req_body=req_body, req_headers=project_headers,
                                                 req_cookies=cookies)
        return project_response.json()['body']

    def update_project(self, org_id, req_body, project_id, cookies):
        api_url = '/api/organizations/' + org_id + '/projects/' + project_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        project_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        project_response = super().send_requests('PUT', url, req_body=req_body, req_headers=project_headers,
                                                 req_cookies=cookies)
        return project_response.json()['body']

    def get_project_by_id(self, org_id, project_id, cookies):
        api_url = '/api/organizations/' + org_id + '/projects/' + project_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        project_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        project_response = super().send_requests('GET', url, None, req_headers=project_headers, req_cookies=cookies)
        return project_response.json()['body']

    def delete_project_by_id(self, org_id, project_id, cookies):
        api_url = '/api/organizations/' + org_id + '/projects/' + project_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        project_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        project_response = super().send_requests('DELETE', url, None, req_headers=project_headers, req_cookies=cookies)
        return project_response.json()

    def search_projects(self, org_id, project_name, page, page_size, cookies):
        api_url = '/api/organizations/' + org_id + '/projects/'
        query_url = ''
        if project_name is not None and project_name != '':
            query_url = 'name=' + project_name
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        project_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        project_response = super().send_requests('GET', url, None, req_headers=project_headers, req_cookies=cookies)
        return project_response.json()['body']

    # The following APIS are about packages
    def get_package_presigned_url(self, org_id, project_id, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/preSingedPutUrl'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        package_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        package_response = super().send_requests('GET', url, None, req_headers=package_headers, req_cookies=cookies)
        return package_response.json()

    def upload_package_from_web(self, api_url, package_file_name, cookies):

        url = self.default_cloud_platform_url + api_url
        file_path = super().resource_file_path + '/' + package_file_name
        files = {'file': (package_file_name, open(file_path, 'rb'))}

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        package_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        package_response = super().send_put_request_with_data_file(url, None, files, req_headers=package_headers,
                                                                   req_cookies=cookies)
        return package_response.json()

    def save_package_info_after_upload(self, org_id, project_id, req_body, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/package/upload'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        package_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        package_response = super().send_requests('POST', url, req_body=req_body, req_headers=package_headers,
                                                 req_cookies=cookies)
        return package_response.json()

    def search_packages(self, org_id, project_id, package_name, package_type, page, page_size, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/packages'
        query_url = ''
        if package_name is not None and package_name != '':
            query_url = 'name=' + package_name
        if package_type is not None and package_type != '':
            query_url = 'pkgType=' + package_type
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        package_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        package_response = super().send_requests('GET', url, None, req_headers=package_headers, req_cookies=cookies)
        return package_response.json()['body']

    def get_package_by_id(self, org_id, package_id, cookies):
        api_url = '/api/organizations/' + org_id + '/package/' + package_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        package_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        package_response = super().send_requests('GET', url, None, req_headers=package_headers, req_cookies=cookies)
        return package_response.json()['body']

    def delete_package_by_id(self, org_id, package_id, cookies):
        api_url = '/api/organizations/' + org_id + '/package/' + package_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        package_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        package_response = super().send_requests('DELETE', url, None, req_headers=package_headers, req_cookies=cookies)
        return package_response.json()

    # The following APIs are about applications
    def create_application(self, org_id, project_id, req_body, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/applications'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('POST', url, req_body=req_body, req_headers=app_headers,
                                             req_cookies=cookies)
        return app_response.json()['body']

    def update_application(self, org_id, app_id, req_body, cookies):
        api_url = '/api/organizations/' + org_id + '/applications/' + app_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('PUT', url, req_body=req_body, req_headers=app_headers,
                                             req_cookies=cookies)
        return app_response.json()['body']

    def delete_application(self, org_id, app_id, cookies):
        api_url = '/api/organizations/' + org_id + '/applications/' + app_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('DELETE', url, req_body=None, req_headers=app_headers,
                                             req_cookies=cookies)
        return app_response.json()

    def search_apps(self, org_id, project_id, app_name, page, page_size, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/applications'
        query_url = ''
        if app_name is not None:
            query_url = 'name=' + app_name
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('GET', url, None, req_headers=app_headers, req_cookies=cookies)
        return app_response.json()['body']

    def get_application_by_id(self, org_id, app_id, cookies):
        api_url = '/api/organizations/' + org_id + '/applications/' + app_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('GET', url, req_body=None, req_headers=app_headers, req_cookies=cookies)
        return app_response.json()['body']

    def release_app(self, org_id, app_id, req_body, cookies):
        api_url = '/api/organizations/' + org_id + '/applications/' + app_id + '/release'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        release_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        release_response = super().send_requests('POST', url, req_body=req_body, req_headers=release_headers,
                                                 req_cookies=cookies)
        return release_response.json()

    def get_release_by_id(self, org_id, release_id, cookies):
        api_url = '/api/organizations/' + org_id + '/releases/' + release_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        release_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        release_response = super().send_requests('GET', url, req_body=None, req_headers=release_headers,
                                                 req_cookies=cookies)
        return release_response.json()['body']

    def search_releases(self, org_id, project_id, page, page_size, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/releases'
        query_url = ''
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        release_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        release_response = super().send_requests('GET', url, None, req_headers=release_headers, req_cookies=cookies)
        return release_response.json()['body']

    def admin_audit_app(self, app_id, req_body, cookies):
        api_url = '/api/admin/app/' + app_id + '/status'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('POST', url, req_body=req_body, req_headers=app_headers,
                                             req_cookies=cookies)
        return app_response.json()

    def admin_search_apps(self, app_name, status_list, page, page_size, cookies):
        api_url = '/api/admin/apps'
        query_url = ''
        if app_name is not None:
            query_url = 'name=' + app_name
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)
        if status_list is not None:
            if len(status_list) > 0:
                for status in status_list:
                    query_url = query_url + '&status=' + status

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('GET', url, None, req_headers=app_headers, req_cookies=cookies)
        return app_response.json()['body']

    # The following APIs are about resources
    def admin_add_resources(self, req_body, cookies):
        api_url = '/api/resource'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('PUT', url, req_body=req_body, req_headers=resource_headers,
                                                  req_cookies=cookies)
        return resource_response.json()

    def admin_get_resource_spec(self, cookies):
        api_url = '/api/resource-spec'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('GET', url, None, req_headers=resource_headers, req_cookies=cookies)
        return resource_response.json()['body']

    def admin_get_resource_by_id(self, resource_id, cookies):
        api_url = '/api/resource/' + resource_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('GET', url, None, req_headers=resource_headers, req_cookies=cookies)
        return resource_response.json()['body']

    def admin_search_resources(self, resource_name, resource_type, page, page_size, cookies):
        api_url = '/api/resources'
        query_url = ''
        if resource_name is not None:
            query_url = 'name=' + resource_name
        if resource_type is not None:
            query_url = 'type=' + resource_type
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('GET', url, None, req_headers=resource_headers, req_cookies=cookies)
        return resource_response.json()['body']

    def admin_update_resource(self, resource_id, req_body, cookies):
        api_url = '/api/resource/' + resource_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('POST', url, req_body=req_body, req_headers=resource_headers,
                                                  req_cookies=cookies)
        return resource_response.json()

    def admin_update_organization_resource(self, org_id, req_body, cookies):
        api_url = '/api/org-resource/' + org_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('POST', url, req_body=req_body, req_headers=resource_headers,
                                                  req_cookies=cookies)
        return resource_response.json()

    def admin_search_organization_resources(self, resource_name, page, page_size, cookies):
        api_url = '/api/org-resources/'
        query_url = ''
        if resource_name is not None:
            query_url = 'name=' + resource_name
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('GET', url, None, req_headers=resource_headers, req_cookies=cookies)
        return resource_response.json()['body']

    def admin_get_organization_resource_by_id(self, org_id, cookies):
        api_url = '/api/org-resource/' + org_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        resource_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        resource_response = super().send_requests('GET', url, None, req_headers=resource_headers, req_cookies=cookies)
        return resource_response.json()['body']

    def org_add_resource_pool(self, req_body, cookies):
        api_url = '/api/pool'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('PUT', url, req_body=req_body, req_headers=pool_headers,
                                              req_cookies=cookies)
        return pool_response.json()

    def org_update_resource_pool(self, req_body, pool_id, cookies):
        api_url = '/api/pool' + pool_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('POST', url, req_body=req_body, req_headers=pool_headers,
                                              req_cookies=cookies)
        return pool_response.json()

    def org_get_resource_pool_by_id(self, pool_id, cookies):
        api_url = '/api/pool/' + pool_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('GET', url, None, req_headers=pool_headers, req_cookies=cookies)
        return pool_response.json()['body']

    def org_delete_resource_pool_by_id(self, pool_id, cookies):
        api_url = '/api/pool/' + pool_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('DELETE', url, None, req_headers=pool_headers, req_cookies=cookies)
        return pool_response.json()

    def org_search_resource_pools(self, pool_name, pool_type, page, page_size, cookies):
        api_url = '/api/pools'
        query_url = ''
        if pool_name is not None:
            query_url = 'name=' + pool_name
        if pool_type is not None:
            query_url = 'type=' + pool_type
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('GET', url, None, req_headers=pool_headers, req_cookies=cookies)
        return pool_response.json()['body']

    def org_resource_pool_check(self, req_body, cookies):
        api_url = '/api/pool_check'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('POST', url, req_body=req_body, req_headers=pool_headers,
                                              req_cookies=cookies)
        return pool_response.json()

    def get_org_pool_select(self, cookies):
        api_url = '/api/pool-select-res'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        pool_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        pool_response = super().send_requests('GET', url, req_body=None, req_headers=pool_headers,
                                              req_cookies=cookies)
        return pool_response.json()['body']

    def search_running_apps(self, org_id, project_id, app_name, page, page_size, cookies):
        api_url = '/api/organizations/' + org_id + '/project/' + project_id + '/app-runs'
        query_url = ''
        if app_name is not None:
            query_url = 'name=' + app_name
        if page > 0:
            query_url = query_url + '&page=' + str(page)
        if page_size > 0:
            query_url = query_url + '&pageSize=' + str(page_size)

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)

        url = self.default_cloud_platform_url + api_url
        if query_url != '':
            x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
            url = self.default_cloud_platform_url + api_url + '?' + query_url
        else:
            x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)

        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('GET', url, None, req_headers=app_headers, req_cookies=cookies)
        return app_response.json()['body']

    def get_running_app_by_id(self, org_id, run_id, cookies):
        api_url = '/api/organizations/' + org_id + '/application-run/' + run_id
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        app_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        app_response = super().send_requests('GET', url, None, req_headers=app_headers, req_cookies=cookies)
        return app_response.json()['body']

    def get_running_app_log_by_id(self, org_id, uuid, cookies):
        api_url = '/api/organizations/' + org_id + '/application-run-log/' + uuid
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, None, time_stamp, dynamic_salt)
        log_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        log_response = super().send_requests('GET', url, None, req_headers=log_headers, req_cookies=cookies)
        return log_response.json()['body']

    def get_running_app_log_download_address(self, org_id, uuid, filename, cookies):
        api_url = '/api/organizations/' + org_id + '/application-run-log/' + uuid + '/preSingedGetUrl'

        query_url = 'name=' + filename
        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, query_url, None, time_stamp, dynamic_salt)
        file_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        url = self.default_cloud_platform_url + api_url + '?' + query_url

        file_response = super().send_requests('GET', url, None, req_headers=file_headers, req_cookies=cookies)
        return file_response.json()['body']

    def start_game_server(self, req_body, cookies):
        api_url = '/api/start-game-server'
        url = self.default_cloud_platform_url + api_url

        time_stamp = util.get_timestamp_millisecond()
        dynamic_salt = self.get_dynamic_salt(cookies)
        x_sign = util.get_signature(api_url, None, json.dumps(req_body), time_stamp, dynamic_salt)
        server_headers = self.set_request_header(time_stamp, x_sign, dynamic_salt)

        server_response = super().send_requests('GET', url, req_body=req_body, req_headers=server_headers,
                                                req_cookies=cookies)
        return server_response.json()['body']

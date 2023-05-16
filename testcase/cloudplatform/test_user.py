import pytest
import datahelper.cloudplatform as cloud_platform_helper
import common.utility as util

automation_org_admin, automation_org_dev = util.get_pre_configured_org()
error_messages = {
    'account_required': 'account为必填字段',
    'invalid_email': 'email必须是一个有效的邮箱',
    'user_not_existed': 'user id 不存在',
    'org_name_required': 'org name为必填字段',
    'org_not_existed': 'org id 不存在',
    'invalid_user_name_or_password': '用户名或者密码错误，请重试',
    'failed_to_add_user': '添加用户失败，请重试',
    'failed_to_update_user': '添加用户失败，请重试'
}
success_message = 'success'
fail_message = 'fail'


class TestUser:

    @pytest.mark.bvt
    def test_user_login_logout(self):
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)
            assert cookies is not None
        finally:
            # logout
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.bvt
    def test_user_login_with_wrong_info(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()

        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
        invalid_account = util.random_str(10)
        user_response = cloud_platform_helper.user_login_return_response(invalid_account, user_encrypt_pw)
        assert error_messages['invalid_user_name_or_password'] in user_response['message']

        invalid_password = util.random_str(10)
        invalid_password = util.get_encrypt_password(public_key, invalid_password)
        user_response = cloud_platform_helper.user_login_return_response(user_name, invalid_password)
        assert error_messages['invalid_user_name_or_password'] in user_response['message']

    @pytest.mark.bvt
    def test_user_create_migu(self):
        user_new_id = ''
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'mg'

            cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']
        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.bvt
    def test_user_create_platform(self):
        user_new_id = ''
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            # add org role : dev
            org_role = 'dev'
            org_roles = {
                org_id: org_role
            }

            username_to_add = 'test_' + util.random_str(10)
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user_with_roles(username_to_add, email, account_type, org_roles, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            org_role_get = user_new['orgRole'][0]
            assert automation_org_admin == org_role_get['orgName']
            assert org_role == org_role_get['role']

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_create_invalid_data(self):
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

            # invalid name
            invalid_name = ''
            email = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'mg'

            user_response = cloud_platform_helper.create_user(invalid_name, email, account_type, cookies)
            assert error_messages['account_required'] in user_response['message']

            # invalid email
            valid_name = 'test_' + util.random_str(10)
            invalid_email = util.random_str(10)
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'
            user_response = cloud_platform_helper.create_user(valid_name, invalid_email, account_type, cookies)
            assert error_messages['invalid_email'] in user_response['message']

            # todo: need to discuss with dev, to let them add such restrictions
            # invalid account type
            # mg: migu用户, inter: 平台用户
            # account_type = '1'
            # user_response = cloud_platform_helper.create_user(valid_name, email, account_type, cookies)

            # create user with invalid org id and role
            invalid_org_id = util.random_str(10)
            invalid_org_role = util.random_str(5)
            org_roles = {
                invalid_org_id: invalid_org_role
            }
            user_response = cloud_platform_helper.create_user_with_roles(valid_name, email, account_type, org_roles,
                                                                         cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']

            # create user with invalid org id but valid role
            org_roles = {
                invalid_org_id: 'dev'
            }
            user_response = cloud_platform_helper.create_user_with_roles(valid_name, email, account_type, org_roles,
                                                                         cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']

            # todo: https://unity3d.atlassian.net/browse/PXCG-1058
            # create user with valid org id but invalid role
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            invalid_org_role = util.random_str(5)
            org_roles = {
                org_id: invalid_org_role
            }
            user_response = cloud_platform_helper.create_user_with_roles(valid_name, email, account_type, org_roles,
                                                                         cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']
        finally:
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_delete_not_existed_user(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)
        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # todo: need to check the error message with dev
        # delete not-existed user
        invalid_user_id = util.random_str(10)
        user_response = cloud_platform_helper.delete_user_by_id(invalid_user_id, cookies)
        assert error_messages['user_not_existed'] in user_response['message']

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_update(self):
        user_new_id = ''
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            username_to_add = 'test_' + util.random_str(10)
            email_to_add = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email_to_add, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email_to_add
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # change user info
            email_to_change = util.random_mail()
            account_type = 'mg'

            cloud_platform_helper.update_user(user_new_id, email_to_change, account_type, None, None, cookies)
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email_to_change
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type

            # add org role : dev
            org_role = 'dev'
            org_roles = {
                org_id: org_role
            }

            cloud_platform_helper.update_user(user_new_id, email_to_change, account_type, org_roles, None, cookies)
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            org_role_get = user_new['orgRole'][0]
            assert automation_org_admin == org_role_get['orgName']
            assert org_role == org_role_get['role']

        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_update_invalid_data(self):
        user_new_id = ''
        cookies = None
        try:
            # user login and get cookies
            user_name, user_pw = util.get_admin_user_name_password()
            public_key = cloud_platform_helper.get_password_public_key()
            user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

            cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

            # get org
            org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
            assert org_admin is not None
            org_id = org_admin['list'][0]['id']

            username_to_add = 'test_' + util.random_str(10)
            email_to_add = util.random_mail()
            # mg: migu用户, inter: 平台用户
            account_type = 'inter'

            cloud_platform_helper.create_user(username_to_add, email_to_add, account_type, cookies)

            # search the newly-created user by account name
            user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
            assert user_new is not None
            assert user_new['account'] == username_to_add
            assert user_new['email'] == email_to_add
            assert user_new['status'] == 1
            assert user_new['accountType'] == account_type
            user_new_id = user_new['id']

            # change user info
            invalid_email = util.random_str(10)

            user_response = cloud_platform_helper.update_user(user_new_id, invalid_email, None, None, None, cookies)
            assert error_messages['invalid_email'] in user_response['message']

            # change to invalid account type
            # todo: need to discuss with dev, to let them add such restrictions
            # invalid account type
            # mg: migu用户, inter: 平台用户
            # account_type = '1'
            # new_email = util.random_mail()
            # user_response = cloud_platform_helper.update_user(user_new_id, new_email, None, None, None, cookies)

            # change to invalid status
            # todo: need to discuss with dev, to let them add such restrictions
            # invalid account type
            # mg: migu用户, inter: 平台用户
            # invalid_status = '100'
            # user_response = cloud_platform_helper.update_user(user_new_id, new_email, None, None, None, cookies)

            # update user with invalid org id and role
            invalid_org_id = util.random_str(10)
            invalid_org_role = util.random_str(5)
            org_roles = {
                invalid_org_id: invalid_org_role
            }
            user_response = cloud_platform_helper.update_user(user_new_id, email_to_add, None, org_roles, None, cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']

            # create user with invalid org id but valid role
            org_roles = {
                invalid_org_id: 'dev'
            }
            user_response = cloud_platform_helper.update_user(user_new_id, email_to_add, None, org_roles, None, cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']

            # todo: https://unity3d.atlassian.net/browse/PXCG-1058
            # update user with valid org id but invalid role
            invalid_org_role = util.random_str(5)
            org_roles = {
                org_id: invalid_org_role
            }
            user_response = cloud_platform_helper.update_user(user_new_id, email_to_add, None, org_roles, None, cookies)
            assert error_messages['failed_to_add_user'] in user_response['message']
        finally:
            if user_new_id != '':
                # delete the user
                cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
            cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_get_by_id(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        user_response = cloud_platform_helper.get_user_by_user_id(user_new_id, cookies)
        user_new = user_response['body']
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type

        # delete the user
        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_get_by_invalid_id(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        user_new_id = user_new['id']

        invalid_user_id = util.random_str(10)
        user_response = cloud_platform_helper.get_user_by_user_id(invalid_user_id, cookies)
        assert error_messages['user_not_existed'] in user_response['message']

        # delete the user
        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_search(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # search user
        search_user_query = {}
        users = cloud_platform_helper.search_users(search_user_query, 0, 0, cookies)
        assert users['total'] >= 1
        user_list = users['list']
        assert len(user_list) >= 1

        # search user with account name
        search_user_query = {'account': username_to_add}
        users = cloud_platform_helper.search_users(search_user_query, 0, 0, cookies)
        assert users['total'] == 1
        user_list = users['list']
        assert len(user_list) == 1
        assert user_list[0]['account'] == username_to_add
        assert user_list[0]['email'] == email
        assert user_list[0]['status'] == 1
        assert user_list[0]['accountType'] == account_type

        # delete the user
        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_change_role(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # get org
        org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
        assert org_admin is not None
        org_id = org_admin['list'][0]['id']

        # change role
        req_body = {
            'orgId': org_id,
            'role': 'dev'
        }
        cloud_platform_helper.user_change_role(user_new_id, req_body, cookies)

        req_body = {
            'orgId': org_id,
            'role': 'org'
        }
        cloud_platform_helper.user_change_role(user_new_id, req_body, cookies)

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_change_role_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # todo
        # get org
        org_admin = cloud_platform_helper.search_org(automation_org_admin, 0, 0, cookies)
        assert org_admin is not None
        org_id = org_admin['list'][0]['id']

        # invalid data
        invalid_user_id = util.random_str(10)
        req_body = {
            'orgId': org_id,
            'role': 'org'
        }
        user_response = cloud_platform_helper.user_change_role(invalid_user_id, req_body, cookies)
        assert error_messages['invalid_email'] in user_response['message']
        req_body = {
            'orgId': org_id,
            'role': 'admin'
        }
        user_response = cloud_platform_helper.user_change_role(user_new_id, req_body, cookies)
        assert error_messages['invalid_email'] in user_response['message']

        # delete the user
        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_bind_unity_account(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # account binding
        unity_account = 'jasonfu@unity3d.com'
        req_body = {
            'id': user_new_id,
            'unityAccount': unity_account
        }
        user_response = cloud_platform_helper.user_bind_unity_account(req_body, cookies)
        assert success_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_bind_unity_account_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # account binding
        invalid_user_id = util.random_str(12)
        invalid_unity_account = 'jasonfu@uni.com'
        req_body = {
            'id': invalid_user_id,
            'unityAccount': invalid_unity_account
        }
        user_response = cloud_platform_helper.user_bind_unity_account(req_body, cookies)
        assert success_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_reset_password(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # account reset password
        old_password = util.random_str(10)
        old_password_encrypt = util.get_encrypt_password(public_key, old_password)
        new_password = util.random_str(10)
        new_password_encrypt = util.get_encrypt_password(public_key, new_password)

        req_body = {
            'oldPassword': old_password_encrypt,
            'newPassword': new_password_encrypt
        }

        user_response = cloud_platform_helper.user_reset_password(user_new_id, req_body, cookies)
        assert success_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_user_reset_password_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        assert user_new is not None
        assert user_new['account'] == username_to_add
        assert user_new['email'] == email
        assert user_new['status'] == 1
        assert user_new['accountType'] == account_type
        user_new_id = user_new['id']

        # account reset password
        # old password is wrong
        old_password = util.random_str(10)
        old_password_encrypt = util.get_encrypt_password(public_key, old_password)
        new_password = util.random_str(10)
        new_password_encrypt = util.get_encrypt_password(public_key, new_password)

        req_body = {
            'oldPassword': old_password_encrypt,
            'newPassword': new_password_encrypt
        }

        user_response = cloud_platform_helper.user_reset_password(user_new_id, req_body, cookies)
        assert success_message in user_response['message']

        # new password is not strong enough
        old_password = util.random_str(10)
        old_password_encrypt = util.get_encrypt_password(public_key, old_password)
        new_password = '11111111'
        new_password_encrypt = util.get_encrypt_password(public_key, new_password)

        req_body = {
            'oldPassword': old_password_encrypt,
            'newPassword': new_password_encrypt
        }

        user_response = cloud_platform_helper.user_reset_password(user_new_id, req_body, cookies)
        assert success_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_send_reset_password_email_to_user(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # send email
        user_response = cloud_platform_helper.send_user_reset_password_email(email, cookies)
        assert success_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_send_reset_password_email_to_user_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # send email
        invalid_email = util.random_str(10)
        user_response = cloud_platform_helper.send_user_reset_password_email(invalid_email, cookies)
        assert error_messages['invalid_email'] in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_reset_password_after_forgotten(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # send email
        user_response = cloud_platform_helper.send_user_reset_password_email(email, cookies)
        assert success_message in user_response['message']

        # reset password according to email verify code
        verify_code = user_response['verifyCode']
        new_password = util.random_str(10)
        new_password_encrypt = util.get_encrypt_password(public_key, new_password)

        req_body = {
            'email': email,
            'verifyCode': verify_code,
            'newPassword': new_password_encrypt
        }
        user_response = cloud_platform_helper.user_reset_password_with_verify_code(req_body, cookies)
        assert success_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_reset_password_after_forgotten_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # change org
        user = cloud_platform_helper.get_user_by_account(user_name, cookies)
        user_id = user['id']

        platform_admin_org = cloud_platform_helper.search_org(automation_platform_admin, 0, 0, cookies)
        assert platform_admin_org is not None
        org_id = platform_admin_org['list'][0]['id']

        cloud_platform_helper.user_change_org(user_id, org_id, cookies)

        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'inter'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # send email
        user_response = cloud_platform_helper.send_user_reset_password_email(email, cookies)
        assert success_message in user_response['message']

        # reset password according to email verify code
        invalid_email = util.random_str(10)
        verify_code = user_response['verifyCode']
        new_password = util.random_str(10)
        new_password_encrypt = util.get_encrypt_password(public_key, new_password)

        req_body = {
            'email': invalid_email,
            'verifyCode': verify_code,
            'newPassword': new_password_encrypt
        }
        user_response = cloud_platform_helper.user_reset_password_with_verify_code(req_body, cookies)
        assert fail_message in user_response['message']

        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_verify_code(self):
        verify_code = cloud_platform_helper.user_get_verify_code(None)
        assert verify_code.status_code is 200

    @pytest.mark.daily
    def test_get_password_public_key(self):
        public_key = cloud_platform_helper.get_password_public_key()
        assert public_key is not None

    @pytest.mark.daily
    def test_get_dynamic_salt(self):
        dynamic_salt = cloud_platform_helper.get_dynamic_salt(None)
        assert dynamic_salt is not None

    @pytest.mark.bvt
    def test_org_add_search(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search organizations without any parameters
        cloud_platform_helper.search_org(None, 0, 0, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1

        org_list = orgs_return['list']
        assert len(org_list) == 1
        assert org_list[0]['name'] == org_name
        assert org_list[0]['description'] == org_description

        # get the organization by ID and then search the organization by its id
        org_id = org_list[0]['id']
        org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
        assert org_return['name'] == org_name
        assert org_return['description'] == org_description

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_delete_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search organizations without any parameters
        cloud_platform_helper.search_org(None, 0, 0, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        org_id = orgs_return['list'][0]['id']

        # delete with invalid org id
        invalid_org_id = util.random_str(10)
        org_response = cloud_platform_helper.delete_org_by_id(invalid_org_id, cookies)
        assert error_messages['org_not_existed'] in org_response['message']

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_update_delete(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_id = orgs_return['list'][0]['id']

        # update the org with the new org name and description
        org_new_name = 'test_' + util.random_str(10)
        org_new_description = util.random_str(20)
        cloud_platform_helper.update_org(org_id, org_new_name, org_new_description, cookies)

        org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
        assert org_return['name'] == org_new_name
        assert org_return['description'] == org_new_description

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 0
        org_list = orgs_return['list']
        assert org_list is None
        org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
        assert org_return is None

    @pytest.mark.daily
    def test_org_update_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_id = orgs_return['list'][0]['id']

        # update the org with the new org name and description
        org_new_name = ''
        org_response = cloud_platform_helper.update_org(org_id, org_new_name, org_description, cookies)
        assert error_messages['org_name_required'] in org_response['message']

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_get_org_by_id(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_id = orgs_return['list'][0]['id']

        # get org with invalid org id
        invalid_org_id = util.random_str(10)
        org_response = cloud_platform_helper.get_org_by_id(invalid_org_id, cookies)
        assert error_messages['org_not_existed'] in org_response['message']

        # correct org id
        org_return = cloud_platform_helper.get_org_by_id(org_id, cookies)
        assert org_return['name'] == org_name
        assert org_return['description'] == org_description

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_binding(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_id = orgs_return['list'][0]['id']

        # add a user
        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'mg'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # org binding 关联类型；1：关联；2：取消
        relate_type = 1
        org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
        assert success_message in org_response['message']

        relate_type = 2
        org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
        assert success_message in org_response['message']

        # delete the user and the org
        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)

    @pytest.mark.daily
    def test_org_binding_invalid_data(self):
        # user login and get cookies
        user_name, user_pw = util.get_admin_user_name_password()
        public_key = cloud_platform_helper.get_password_public_key()
        user_encrypt_pw = util.get_encrypt_password(public_key, user_pw)

        cookies = cloud_platform_helper.user_login(user_name, user_encrypt_pw)

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_id = orgs_return['list'][0]['id']

        # add a user
        username_to_add = 'test_' + util.random_str(10)
        email = util.random_mail()
        # mg: migu用户, inter: 平台用户
        account_type = 'mg'

        cloud_platform_helper.create_user(username_to_add, email, account_type, cookies)

        # search the newly-created user by account name
        user_new = cloud_platform_helper.get_user_by_account(username_to_add, cookies)
        user_new_id = user_new['id']

        # org binding 关联类型；1：关联；2：取消
        relate_type = 5
        org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
        assert fail_message in org_response['message']

        relate_type = 2
        org_response = cloud_platform_helper.org_binding(username_to_add, org_id, relate_type, cookies)
        assert fail_message in org_response['message']

        relate_type = 1
        invalid_user = util.random_str(10)
        org_response = cloud_platform_helper.org_binding(invalid_user, org_id, relate_type, cookies)
        assert fail_message in org_response['message']

        invalid_org_id = util.random_str(10)
        org_response = cloud_platform_helper.org_binding(username_to_add, invalid_org_id, relate_type, cookies)
        assert fail_message in org_response['message']

        # delete the user and the org
        cloud_platform_helper.delete_user_by_id(user_new_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)

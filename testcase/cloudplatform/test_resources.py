import pytest
import datahelper.cloudplatform as cloud_platform_helper
import common.utility as util

automation_org_admin, automation_org_dev = util.get_pre_configured_org()
error_messages = {
    'resource_name_required': 'resource name为必填字段',
    'resource_type_incorrect': 'resource type不正确',
    'resource_spec_not_existed': 'resource spec不存在',
    'total_size_not_correct': 'total size 必须大于0',
    'resource_description_required': 'resource description为必填字段'
}
success_message = 'success'
fail_message = 'fail'


class TestUserOrg:
    @pytest.mark.bvt
    def test_admin_create_resource(self):
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

        # create resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_create_resource_invalid_data(self):
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

        # create resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        # resource_name is null
        resource_name = ''
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_name_required'] in resource_created['message']

        # resource type is incorrect
        resource_name = 'test_' + util.random_str(10)
        resource_type = 'invalid_type'
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_type_incorrect'] in resource_created['message']

        # spec id is incorrect
        resource_name = 'test_' + util.random_str(10)
        resource_type = '1'
        resource_spec_id = 'invalid spec id'
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_spec_not_existed'] in resource_created['message']

        # total size is not correct
        resource_name = 'test_' + util.random_str(10)
        resource_type = '1'
        resource_spec_id = resource_spec[0]['id']
        total_size = 0
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['total_size_not_correct'] in resource_created['message']

        # description is null
        resource_name = 'test_' + util.random_str(10)
        resource_type = '1'
        resource_spec_id = resource_spec[0]['id']
        total_size = util.random_int(50, 100)
        resource_description = ''
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_description_required'] in resource_created['message']

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_update_resource(self):
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

        # create resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        # update the resource
        resource_name_update = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type_update = '2'
        total_size_update = util.random_int(50, 100)
        resource_description_update = util.random_str(20)

        req_body = {
            'name': resource_name_update,
            'type': resource_type_update,
            'specId': resource_spec_id,
            'total': total_size_update,
            'description': resource_description_update
        }
        resource_created = cloud_platform_helper.admin_update_resource(resource_id, req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_get_resource_by_id(resource_id, cookies)
        assert resource_created['name'] == resource_name_update
        assert resource_created['type'] == resource_type_update
        assert resource_created['description'] == resource_description_update
        assert resource_created['total'] == total_size_update

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_update_resource_invalid_data(self):
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

        # create resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        # update the resource
        # resource_name is null
        resource_name = ''
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_name_required'] in resource_created['message']

        # resource type is incorrect
        resource_name = 'test_' + util.random_str(10)
        resource_type = 'invalid_type'
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_type_incorrect'] in resource_created['message']

        # spec id is incorrect
        resource_name = 'test_' + util.random_str(10)
        resource_type = '1'
        resource_spec_id = 'invalid spec id'
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_spec_not_existed'] in resource_created['message']

        # total size is not correct
        resource_name = 'test_' + util.random_str(10)
        resource_type = '1'
        resource_spec_id = resource_spec[0]['id']
        total_size = 0
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['total_size_not_correct'] in resource_created['message']

        # description is null
        resource_name = 'test_' + util.random_str(10)
        resource_type = '1'
        resource_spec_id = resource_spec[0]['id']
        total_size = util.random_int(50, 100)
        resource_description = ''
        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert error_messages['resource_description_required'] in resource_created['message']

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_get_resource_by_id(self):
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

        # create resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        # get the resource by id
        resource_created = cloud_platform_helper.admin_get_resource_by_id(resource_id, cookies)
        assert resource_created['name'] == resource_name
        assert resource_created['type'] == resource_type
        assert resource_created['description'] == resource_description
        assert resource_created['total'] == total_size

        # get the resource by invalid id
        resource_created = cloud_platform_helper.admin_get_resource_by_id('invalid_id', cookies)
        assert fail_message in resource_created['message']

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_search_resources(self):
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

        # create resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size

        # no search query
        resource_created = cloud_platform_helper.admin_search_resources(None, None, 0, 0, cookies)
        assert resource_created['total'] >= 1

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_update_org_resource(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_get_org_resource_by_id(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        org_resource = cloud_platform_helper.admin_get_organization_resource_by_id(org_id, cookies)
        assert success_message in org_resource['message']

        # invalid org id
        org_resource = cloud_platform_helper.admin_get_organization_resource_by_id('invalid_id', cookies)
        assert fail_message in org_resource['message']
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_search_org_resources(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_add_resource_pool(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_add_resource_pool_invalid_data(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_delete_resource_pool_by_id(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_update_resource_pool(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_update_resource_pool_invalid_data(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_get_resource_pool_by_id(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_search_resource_pools(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_admin_resource_pool_check(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_admin_resource_pool_check_invalid_data(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource nname
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

    @pytest.mark.daily
    def test_org_admin_get_available_resource_pool(self):
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

        # add an organization
        org_name = 'test_' + util.random_str(10)
        org_description = util.random_str(20)
        cloud_platform_helper.create_org(org_name, org_description, cookies)

        # search the organization by name
        orgs_return = cloud_platform_helper.search_org(org_name, 0, 0, cookies)
        assert orgs_return['total'] == 1
        org_list = orgs_return['list']
        org_id = org_list[0]['id']

        # create a resource
        # get resource spec firstly
        resource_spec = cloud_platform_helper.admin_get_resource_spec(cookies)
        resource_spec_id = resource_spec[0]['id']
        resource_name = 'test_' + util.random_str(10)
        # 资源类型 1：定量；2：弹性
        resource_type = '1'
        total_size = util.random_int(50, 100)
        resource_description = util.random_str(20)

        req_body = {
            'name': resource_name,
            'type': resource_type,
            'specId': resource_spec_id,
            'total': total_size,
            'description': resource_description
        }
        resource_created = cloud_platform_helper.admin_add_resources(req_body, cookies)
        assert success_message in resource_created['message']

        # search the newly-created resource by name
        resource_created = cloud_platform_helper.admin_search_resources(resource_name, resource_type, 0, 0, cookies)
        assert resource_created['total'] == 1
        resource_list = resource_created['list']
        assert len(resource_list) == 1
        assert resource_list[0]['name'] == resource_name
        assert resource_list[0]['type'] == resource_type
        assert resource_list[0]['description'] == resource_description
        assert resource_list[0]['total'] == total_size
        resource_id = resource_list[0]['id']

        req_body = {
            "quotaRes": [
                {
                    "resourceId": resource_id,
                    "name": resource_name,
                    "capacity": total_size - 10
                }
            ]
        }

        add_org_resource = cloud_platform_helper.admin_update_organization_resource(org_id, req_body, cookies)
        assert success_message in add_org_resource['message']

        # search by resource name
        org_resource = cloud_platform_helper.admin_search_organization_resources(resource_name, 0, 0, cookies)
        assert org_resource['total'] == 1

        # get resource list
        org_resource =  cloud_platform_helper.get_org_pool_select(cookies)
        assert success_message in org_resource['message']

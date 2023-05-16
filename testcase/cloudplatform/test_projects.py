
import pytest
import datahelper.cloudplatform as cloud_platform_helper
import common.utility as util

error_messages = {
    'project_name_required': 'project name为必填字段',
    'project_not_existed': 'project id 不存在',
    'org_not_existed': 'org id 不存在',
    'package_not_existed': 'package id 不存在'
}
success_message = 'success'
fail_message = 'fail'


class TestProjects:

    @pytest.mark.bvt
    def test_projects_create(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_created['id'], cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_create_invalid_data(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = ''
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert error_messages['project_name_required'] in project_created['message']

        # delete the org
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_delete(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id

        # delete the project with invalid id
        invalid_project_id = util.random_str(10)
        project_response = cloud_platform_helper.delete_project_by_id(org_id, invalid_project_id, cookies)
        assert error_messages['project_not_existed'] in project_response['message']

        invalid_org_id = util.random_str(10)
        project_response = cloud_platform_helper.delete_project_by_id(invalid_org_id, project_created['id'], cookies)
        assert error_messages['org_not_existed'] in project_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_created['id'], cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_update(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # update the project name and description
        new_project_name = 'test_project_' + util.random_str(10)
        new_project_description = util.random_str(10)
        project_updated = cloud_platform_helper.update_project(org_id, project_id, new_project_name,
                                                               new_project_description, cookies)
        assert project_updated['displayName'] == new_project_name
        assert project_updated['description'] == new_project_description

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_projects_update_invalid_data(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # update the project name and description
        new_project_name = ''
        new_project_description = util.random_str(10)
        project_updated = cloud_platform_helper.update_project(org_id, project_id, new_project_name,
                                                               new_project_description, cookies)
        assert error_messages['project_name_required'] in project_updated['message']

        project_created = cloud_platform_helper.get_project_by_id(org_id, project_id, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_single_project(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # delete the project with invalid id
        project_get = cloud_platform_helper.get_project_by_id(org_id, project_id, cookies)
        assert project_get['displayName'] == project_name
        assert project_get['description'] == project_description
        assert project_get['orgId'] == org_id

        invalid_project_id = util.random_str(10)
        project_response = cloud_platform_helper.get_project_by_id(org_id, invalid_project_id, cookies)
        assert error_messages['project_not_existed'] in project_response['message']

        invalid_org_id = util.random_str(10)
        project_response = cloud_platform_helper.get_project_by_id(invalid_org_id, project_created['id'], cookies)
        assert error_messages['org_not_existed'] in project_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_projects(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # search all the projects
        projects = cloud_platform_helper.search_projects(org_id, None, 0, 0,  cookies)
        assert projects['total'] == 1
        project_list = projects['list']
        assert len(project_list) == 1
        assert project_list[0]['displayName'] == project_name
        assert project_list[0]['description'] == project_description
        assert project_list[0]['orgId'] == org_id

        # search projects with project name
        projects = cloud_platform_helper.search_projects(org_id, project_name, 0, 0, cookies)
        assert projects['total'] == 1
        project_list = projects['list']
        assert len(project_list) == 1
        assert project_list[0]['displayName'] == project_name
        assert project_list[0]['description'] == project_description
        assert project_list[0]['orgId'] == org_id

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    # package
    @pytest.mark.daily
    def test_upload_package(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # get the package pre_signed url
        package_response = cloud_platform_helper.get_package_pre_signed_address(org_id, project_id, cookies)
        assert success_message in package_response['message']
        pre_signed_url = package_response['body']['url']
        package_id = package_response['body']['packageId']
        file_name = 'server.zip'
        package_response = cloud_platform_helper.upload_package_from_web(pre_signed_url, file_name, cookies)
        assert success_message in package_response['message']
        req_body = {
            'pkgId': package_id,
            'md5': '0396f8c7ec20260c4751fb362fd48064',
            'fileName': file_name,
            'size': '1674352',
            'pkgType': 'server',
            'version': '0.0.1'
        }
        package_response = cloud_platform_helper.save_package_info_after_upload(org_id, project_id, req_body, cookies)
        assert success_message in package_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_delete_package(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # get the package pre_signed url
        package_response = cloud_platform_helper.get_package_pre_signed_address(org_id, project_id, cookies)
        assert success_message in package_response['message']
        pre_signed_url = package_response['body']['url']
        package_id = package_response['body']['packageId']
        file_name = 'server.zip'
        package_response = cloud_platform_helper.upload_package_from_web(pre_signed_url, file_name, cookies)
        assert success_message in package_response['message']
        req_body = {
            'pkgId': package_id,
            'md5': '0396f8c7ec20260c4751fb362fd48064',
            'fileName': file_name,
            'size': '1674352',
            'pkgType': 'server',
            'version': '0.0.1'
        }
        package_response = cloud_platform_helper.save_package_info_after_upload(org_id, project_id, req_body, cookies)
        assert success_message in package_response['message']

        # delete the package with invalid id
        invalid_package_id = util.random_str(10)
        package_response = cloud_platform_helper.delete_package_by_id(org_id, invalid_package_id, cookies)
        assert error_messages['package_not_existed'] in package_response['message']

        invalid_org_id = util.random_str(10)
        package_response = cloud_platform_helper.delete_package_by_id(invalid_org_id, package_id, cookies)
        assert error_messages['org_not_existed'] in package_response['message']

        # delete the package
        package_response = cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
        assert success_message in package_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_package_by_id(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # get the package pre_signed url
        package_response = cloud_platform_helper.get_package_pre_signed_address(org_id, project_id, cookies)
        assert success_message in package_response['message']
        pre_signed_url = package_response['body']['url']
        package_id = package_response['body']['packageId']
        file_name = 'server.zip'
        package_response = cloud_platform_helper.upload_package_from_web(pre_signed_url, file_name, cookies)
        assert success_message in package_response['message']
        req_body = {
            'pkgId': package_id,
            'md5': '0396f8c7ec20260c4751fb362fd48064',
            'fileName': file_name,
            'size': '1674352',
            'pkgType': 'server',
            'version': '0.0.1'
        }
        package_response = cloud_platform_helper.save_package_info_after_upload(org_id, project_id, req_body, cookies)
        assert success_message in package_response['message']

        # get the package with invalid id
        invalid_package_id = util.random_str(10)
        package_response = cloud_platform_helper.get_package_by_id(org_id, invalid_package_id, cookies)
        assert error_messages['package_not_existed'] in package_response['message']

        invalid_org_id = util.random_str(10)
        package_response = cloud_platform_helper.get_package_by_id(invalid_org_id, package_id, cookies)
        assert error_messages['org_not_existed'] in package_response['message']

        # get the package
        package_response = cloud_platform_helper.get_package_by_id(org_id, package_id, cookies)
        assert success_message in package_response['message']
        package_response['body']['displayName'] = file_name

        # delete the created org and the project
        cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_packages(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # get the package pre_signed url
        package_response = cloud_platform_helper.get_package_pre_signed_address(org_id, project_id, cookies)
        assert success_message in package_response['message']
        pre_signed_url = package_response['body']['url']
        package_id = package_response['body']['packageId']
        file_name = 'server.zip'
        package_response = cloud_platform_helper.upload_package_from_web(pre_signed_url, file_name, cookies)
        assert success_message in package_response['message']
        req_body = {
            'pkgId': package_id,
            'md5': '0396f8c7ec20260c4751fb362fd48064',
            'fileName': file_name,
            'size': '1674352',
            'pkgType': 'server',
            'version': '0.0.1'
        }
        package_response = cloud_platform_helper.save_package_info_after_upload(org_id, project_id, req_body, cookies)
        assert success_message in package_response['message']

        # search all the packages
        package_response = cloud_platform_helper.search_packages(org_id, project_id, None, None, 0, 0, cookies)
        assert package_response['total'] == 1

        package_list = package_response['list']
        assert len(package_list) == 1
        assert package_list[0]['displayName'] == file_name

        # search the package with name
        package_response = cloud_platform_helper.search_packages(org_id, project_id, file_name, None, 0, 0, cookies)
        assert package_response['total'] == 1

        package_list = package_response['list']
        assert len(package_list) == 1
        assert package_list[0]['displayName'] == file_name

        # search with invalid name and type
        package_response = cloud_platform_helper.search_packages(org_id, project_id, 'invalid_name', 'invalid_type', 0,
                                                                 0, cookies)
        assert package_response['total'] == 0

        # delete the created org and the project
        cloud_platform_helper.delete_package_by_id(org_id, package_id, cookies)
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    # applications
    @pytest.mark.daily
    def test_create_application(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_create_application_invalid_data(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app with invalid name
        app_name = ''
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert fail_message in app_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_update_application(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # update app info
        app_name_update = util.random_str(10)
        app_description_update = util.random_str(20)

        req_body = {
            'displayName': app_name_update,
            'description': app_description_update,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }
        app_response = cloud_platform_helper.update_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_update_application_invalid_data(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # update app info:
        app_name_update = ''
        app_description_update = util.random_str(20)

        req_body = {
            'displayName': app_name_update,
            'description': app_description_update,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }
        app_response = cloud_platform_helper.update_application(org_id, project_id, req_body, cookies)
        assert fail_message in app_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_delete_application_by_id(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # delete the app with invalid id
        app_response = cloud_platform_helper.delete_application(org_id, project_id, cookies)
        assert fail_message in app_response['message']

        # delete the app with correct id
        app_response = cloud_platform_helper.delete_application(org_id, project_id, cookies)
        assert success_message in app_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_delete_application_by_id(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # get the app with invalid id
        app_response = cloud_platform_helper.get_application_by_id(org_id, project_id, cookies)
        assert fail_message in app_response['message']

        # delete the app with correct id
        app_response = cloud_platform_helper.get_application_by_id(org_id, project_id, cookies)
        assert success_message in app_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_applications(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        # get the apps
        app_response = cloud_platform_helper.search_apps(org_id, project_id, None, 0, 0, cookies)
        assert success_message in app_response['message']

        # get the apps with app name
        app_response = cloud_platform_helper.search_apps(org_id, project_id, app_name, 0, 0, cookies)
        assert success_message in app_response['message']
        assert app_response['total'] == 1
        app_list = orgs_return['list']
        assert len(app_list) == 1
        assert app_list[0]['name'] == app_name
        assert app_list[0]['description'] == app_description

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_release_application(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        app_response = cloud_platform_helper.search_apps(org_id, project_id, app_name, 0, 0, cookies)
        assert success_message in app_response['message']
        assert app_response['total'] == 1
        app_list = orgs_return['list']
        assert len(app_list) == 1
        assert app_list[0]['name'] == app_name
        assert app_list[0]['description'] == app_description

        app_id = app_list[0]['id']
        req_body = {
            'version': '1.0.0',
            'desc': util.random_str(20)
        }

        release_response = cloud_platform_helper.release_app(org_id, app_id, req_body, cookies)
        assert success_message in release_response['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_search_application_releases(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        app_response = cloud_platform_helper.search_apps(org_id, project_id, app_name, 0, 0, cookies)
        assert success_message in app_response['message']
        assert app_response['total'] == 1
        app_list = orgs_return['list']
        assert len(app_list) == 1
        assert app_list[0]['name'] == app_name
        assert app_list[0]['description'] == app_description

        app_id = app_list[0]['id']
        req_body = {
            'version': '1.0.0',
            'desc': util.random_str(20)
        }

        release_response = cloud_platform_helper.release_app(org_id, app_id, req_body, cookies)
        assert success_message in release_response['message']

        releases = cloud_platform_helper.search_releases(org_id, project_id, 0, 0, cookies)
        assert success_message in releases['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_get_application_release_by_id(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        app_response = cloud_platform_helper.search_apps(org_id, project_id, app_name, 0, 0, cookies)
        assert success_message in app_response['message']
        assert app_response['total'] == 1
        app_list = orgs_return['list']
        assert len(app_list) == 1
        assert app_list[0]['name'] == app_name
        assert app_list[0]['description'] == app_description

        app_id = app_list[0]['id']
        req_body = {
            'version': '1.0.0',
            'desc': util.random_str(20)
        }

        release_response = cloud_platform_helper.release_app(org_id, app_id, req_body, cookies)
        assert success_message in release_response['message']

        releases = cloud_platform_helper.search_releases(org_id, project_id, 0, 0, cookies)
        assert success_message in releases['message']
        release_id = releases['body']['list'][0]['id']
        release = cloud_platform_helper.get_release_by_id(org_id, release_id, cookies)
        assert success_message in release['message']

        # get release by invalid id
        release = cloud_platform_helper.get_release_by_id(org_id, 'invalid_id', cookies)
        assert fail_message in release['message']

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)

    @pytest.mark.daily
    def test_admin_audit_release_by_id(self):
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
        org_id = org_list[0]['id']

        # add a project
        project_name = 'test_project_' + util.random_str(10)
        project_description = util.random_str(20)
        project_created = cloud_platform_helper.create_project(org_id, project_name, project_description, cookies)
        assert project_created['displayName'] == project_name
        assert project_created['description'] == project_description
        assert project_created['orgId'] == org_id
        project_id = project_created['id']

        # add an app
        app_name = util.random_str(10)
        app_description = util.random_str(20)

        req_body = {
            'displayName': app_name,
            'description': app_description,
            'enableRendering': True,
            'renderingNodeNumber': 4
        }

        app_response = cloud_platform_helper.create_application(org_id, project_id, req_body, cookies)
        assert success_message in app_response['message']

        app_response = cloud_platform_helper.search_apps(org_id, project_id, app_name, 0, 0, cookies)
        assert success_message in app_response['message']
        assert app_response['total'] == 1
        app_list = orgs_return['list']
        assert len(app_list) == 1
        assert app_list[0]['name'] == app_name
        assert app_list[0]['description'] == app_description

        app_id = app_list[0]['id']
        req_body = {
            'version': '1.0.0',
            'desc': util.random_str(20)
        }

        release_response = cloud_platform_helper.release_app(org_id, app_id, req_body, cookies)
        assert success_message in release_response['message']

        releases = cloud_platform_helper.search_releases(org_id, project_id, 0, 0, cookies)
        assert success_message in releases['message']
        release_id = releases['body']['list'][0]['id']
        release = cloud_platform_helper.get_release_by_id(org_id, release_id, cookies)
        assert success_message in release['message']

        # audit [批准=released,拒绝=rejected,上架=onsale,下架=offsale]
        req_body = {
            'status': 'rejected'
        }

        # delete the created org and the project
        cloud_platform_helper.delete_project_by_id(org_id, project_id, cookies)
        cloud_platform_helper.delete_org_by_id(org_id, cookies)
        cloud_platform_helper.user_logout(cookies)
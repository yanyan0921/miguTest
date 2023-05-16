from rest.cloudplatform.cloudplatform import CloudPlatformService

cloud_platform_service = CloudPlatformService()


def dict_ext(d1, d2):
    result = dict(d1)
    result.update(d2)
    return result


# Users
def user_get_verify_code(cookies):
    return cloud_platform_service.user_get_verify_code(cookies)


def get_password_public_key():
    return cloud_platform_service.user_get_password_public_key()


def get_dynamic_salt(cookies):
    return cloud_platform_service.get_dynamic_salt(cookies)


def user_login(user_name, user_pw):
    req_body = {
        'account': user_name,
        'password': user_pw
    }
    return cloud_platform_service.user_login(req_body)


def user_login_return_response(user_name, user_pw):
    req_body = {
        'account': user_name,
        'password': user_pw
    }
    return cloud_platform_service.user_login_response(req_body)


def user_logout(cookies):
    return cloud_platform_service.user_logout(cookies)


def create_user(account_name, email, account_type, cookies):
    req_body = {
        'account': account_name,
        'email': email,
        'accountType': account_type
    }
    return cloud_platform_service.create_user(req_body, cookies)


def create_user_with_roles(account_name, email, account_type, org_roles, cookies):
    req_body = {
        'account': account_name,
        'email': email,
        'accountType': account_type
    }

    if org_roles is not None:
        req_body.update({'orgRole': org_roles})

    return cloud_platform_service.create_user(req_body, cookies)


def update_user(user_id, email, account_type, org_roles, status, cookies):
    req_body = {
        'email': email
    }

    if account_type is not None and account_type != '':
        req_body.update({'accountType': account_type})
    if org_roles is not None:
        req_body.update({'orgRole': org_roles})
    if status is not None and status != '':
        req_body.update({'status': status})

    return cloud_platform_service.update_user_info(req_body, user_id, cookies)


def get_user_by_account(account_name, cookies):
    return cloud_platform_service.get_single_user_info_by_account(account_name, cookies)


def get_user_by_user_id(user_id, cookies):
    return cloud_platform_service.get_single_user_info_by_id(user_id, cookies)


# The default page is 1 and default page_size is 10 in dev code. we could just set page = 0 and page_size = 0 in
# our test cases
def search_users(search_user_query, page, page_size, cookies):
    return cloud_platform_service.search_users(search_user_query, page, page_size, cookies)


def user_change_role(user_id, change_role_body, cookies):
    return cloud_platform_service.user_change_role(user_id, change_role_body, cookies)


def user_bind_unity_account(req_body, cookies):
    return cloud_platform_service.user_bind_unity_account(req_body, cookies)


def user_reset_password(user_id, req_body, cookies):
    return cloud_platform_service.user_reset_password(user_id, req_body, cookies)


def send_user_reset_password_email(account_email, cookies):
    req_body = {
        'account': account_email
    }
    return cloud_platform_service.user_send_reset_email(req_body, cookies)


def user_reset_password_with_verify_code(req_body, cookies):
    return cloud_platform_service.user_forget_password(req_body, cookies)


def delete_user_by_id(user_id, cookies):
    return cloud_platform_service.delete_user_by_id(user_id, cookies)


# Organizations
def create_org(org_name, org_description, cookies):
    req_body = {
        'name': org_name,
        'description': org_description
    }
    return cloud_platform_service.create_organization(req_body, cookies)


# The default page is 1 and default page_size is 10 in dev code. we could just set page = 0 and page_size = 0 in
# our test cases
def search_org(org_name, page, page_size, cookies):
    return cloud_platform_service.search_organization(org_name, page, page_size, cookies)


def get_org_by_id(org_id, cookies):
    return cloud_platform_service.get_organization_by_id(org_id, cookies)


def update_org(org_id, org_new_name, org_new_description, cookies):
    req_body = {
        'name': org_new_name,
        'description': org_new_description
    }
    return cloud_platform_service.update_organization(org_id, req_body, cookies)


def delete_org_by_id(org_id, cookies):
    return cloud_platform_service.delete_organization_by_id(org_id, cookies)


def user_change_org(user_id, org_id, cookies):
    return cloud_platform_service.user_change_org(user_id, org_id, cookies)


def org_binding(account_name, org_id, relate_type, cookies):
    req_body = {
        'account': account_name,
        'orgId': org_id,
        'relateType': relate_type
    }
    return cloud_platform_service.bind_organization(req_body, cookies)


# Projects
def create_project(org_id, project_name, project_description, cookies):
    req_body = {
        'displayName': project_name,
        'description': project_description
    }
    return cloud_platform_service.create_project(org_id, req_body, cookies)


def update_project(org_id, project_id, project_name, project_description, cookies):
    req_body = {
        'displayName': project_name,
        'description': project_description
    }
    return cloud_platform_service.update_project(org_id, req_body, project_id, cookies)


def get_project_by_id(org_id, project_id, cookies):
    return cloud_platform_service.get_project_by_id(org_id, project_id, cookies)


def delete_project_by_id(org_id, project_id, cookies):
    return cloud_platform_service.delete_project_by_id(org_id, project_id, cookies)


def search_projects(org_id, project_name, page, page_size, cookies):
    return cloud_platform_service.search_projects(org_id, project_name, page, page_size, cookies)


# package
def get_package_pre_signed_address(org_id, project_id, cookies):
    return cloud_platform_service.get_package_presigned_url(org_id, project_id, cookies)


def upload_package_from_web(api_url, package_file_name, cookies):
    return cloud_platform_service.upload_package_from_web(api_url, package_file_name, cookies)


def save_package_info_after_upload(org_id, project_id, req_body, cookies):
    return cloud_platform_service.save_package_info_after_upload(org_id, project_id, req_body, cookies)


def search_packages(org_id, project_id, package_name, package_type, page, page_size, cookies):
    return cloud_platform_service.search_packages(org_id, project_id, package_name, package_type, page, page_size,
                                                  cookies)


def get_package_by_id(org_id, package_id, cookies):
    return cloud_platform_service.get_package_by_id(org_id, package_id, cookies)


def delete_package_by_id(org_id, package_id, cookies):
    return cloud_platform_service.delete_package_by_id(org_id, package_id, cookies)


# applications
def create_application(org_id, project_id, req_body, cookies):
    return cloud_platform_service.create_application(org_id, project_id, req_body, cookies)


def update_application(org_id, app_id, req_body, cookies):
    return cloud_platform_service.update_application(org_id, app_id, req_body, cookies)


def delete_application(org_id, app_id, cookies):
    return cloud_platform_service.delete_application(org_id, app_id, cookies)


def search_apps(org_id, project_id, app_name, page, page_size, cookies):
    return cloud_platform_service.search_apps(org_id, project_id, app_name, page, page_size, cookies)


def get_application_by_id(org_id, app_id, cookies):
    return cloud_platform_service.get_application_by_id(org_id, app_id, cookies)


def release_app(org_id, app_id, req_body, cookies):
    return cloud_platform_service.release_app(org_id, app_id, req_body, cookies)


def get_release_by_id(org_id, release_id, cookies):
    return cloud_platform_service.get_release_by_id(org_id, release_id, cookies)


def search_releases(org_id, project_id, page, page_size, cookies):
    return cloud_platform_service.search_releases(org_id, project_id, page, page_size, cookies)


def admin_audit_app(app_id, req_body, cookies):
    return cloud_platform_service.admin_audit_app(app_id, req_body, cookies)


def admin_search_apps(app_name, status_list, page, page_size, cookies):
    return cloud_platform_service.admin_search_apps(app_name, status_list, page, page_size, cookies)


# running app
def search_running_apps(org_id, project_id, app_name, page, page_size, cookies):
    return cloud_platform_service.search_running_apps(org_id, project_id, app_name, page, page_size, cookies)


def get_running_app_by_id(org_id, run_id, cookies):
    return cloud_platform_service.get_running_app_by_id(org_id, run_id, cookies)


def get_running_app_log_by_id(org_id, uuid, cookies):
    return cloud_platform_service.get_running_app_log_by_id(org_id, uuid, cookies)


def get_running_app_log_download_address(org_id, uuid, filename, cookies):
    return cloud_platform_service.get_running_app_log_download_address(org_id, uuid, filename, cookies)


def start_game_server(req_body, cookies):
    return cloud_platform_service.start_game_server(req_body, cookies)


# resources
def admin_add_resources(req_body, cookies):
    return cloud_platform_service.admin_add_resources(req_body, cookies)


def admin_get_resource_spec(cookies):
    return cloud_platform_service.admin_get_resource_spec(cookies)


def admin_get_resource_by_id(resource_id, cookies):
    return cloud_platform_service.admin_get_resource_by_id(resource_id, cookies)


def admin_search_resources(resource_name, resource_type, page, page_size, cookies):
    return cloud_platform_service.admin_search_resources(resource_name, resource_type, page, page_size, cookies)


def admin_update_resource(resource_id, req_body, cookies):
    return cloud_platform_service.admin_update_resource(resource_id, req_body, cookies)


def admin_update_organization_resource(org_id, req_body, cookies):
    return cloud_platform_service.admin_update_organization_resource(org_id, req_body, cookies)


def admin_search_organization_resources(resource_name, page, page_size, cookies):
    return cloud_platform_service.admin_search_organization_resources(resource_name, page, page_size, cookies)


def admin_get_organization_resource_by_id(org_id, cookies):
    return cloud_platform_service.admin_get_organization_resource_by_id(org_id, cookies)


def org_add_resource_pool(req_body, cookies):
    return cloud_platform_service.org_add_resource_pool(req_body, cookies)


def org_update_resource_pool(req_body, pool_id, cookies):
    return cloud_platform_service.org_update_resource_pool(req_body, pool_id, cookies)


def org_get_resource_pool_by_id(pool_id, cookies):
    return cloud_platform_service.org_get_resource_pool_by_id(pool_id, cookies)


def org_delete_resource_pool_by_id(pool_id, cookies):
    return cloud_platform_service.org_delete_resource_pool_by_id(pool_id, cookies)


def org_search_resource_pools(pool_name, pool_type, page, page_size, cookies):
    return org_search_resource_pools(pool_name, pool_type, page, page_size, cookies)


def org_resource_pool_check(req_body, cookies):
    return cloud_platform_service.org_resource_pool_check(req_body, cookies)


def get_org_pool_select(cookies):
    return cloud_platform_service.get_org_pool_select(cookies)

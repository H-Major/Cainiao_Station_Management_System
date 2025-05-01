import os
create_ui = ["python -m PyQt5.uic.pyuic window.ui -o window_UI.py ",
             "python -m PyQt5.uic.pyuic manage_user.ui -o manage_user_UI.py ",
             "python -m PyQt5.uic.pyuic manage_package.ui -o manage_package_UI.py ",
             "python -m PyQt5.uic.pyuic manage_admin.ui -o manage_admin_UI.py ",
             "python -m PyQt5.uic.pyuic manage_grant.ui -o manage_grant_UI.py "
             ]
for sh in create_ui:
    print("执行shell:", sh)
    os.system(sh)

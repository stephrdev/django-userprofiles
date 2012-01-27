django-userprofiles
===================

django-userprofiles is a simple registration app with some extra features.


Registration settings
---------------------

`USERPROFILES_CHECK_UNIQUE_EMAIL`
    If enabled, the form checks if the user provided email is already in use.
    (useful if you want to allow user to log in with their email address)

`USERPROFILES_DOUBLE_CHECK_EMAIL`
    If enabled, the form shows two email fields. The user is required to enter
    the same email address twice.

`USERPROFILES_DOUBLE_CHECK_PASSWORD`
    If enabled, the form shows two password fields. The user is required to
    enter the same password twice to proceed.

`USERPROFILES_REGISTRATION_FULLNAME`
    If enabled, the registration form adds two fields for first and last name.

`USERPROFILES_REGISTRATION_FORM`
    You can override the default registration form by changing this setting.
    Defaults to 'userprofiles.forms.RegistrationForm'

`USERPROFILES_USE_ACCOUNT_VERIFICATION`
    This app provides a mechanism to verify user accounts by sending an email
    with an activation link. To use the account verification you have to add
    `userprofiles.contrib.accountverification` to your `INSTALLED_APPS` in
    order toto enable the verification.

`USERPROFILES_ACCOUNT_VERIFICATION_DAYS`
    Defines the amount of days a user has to activate his account. Defaults to
    7.


Profile settings
----------------

django-userprofiles is prepared to work with profile models and provides some
features to make it easy to manage these profiles.

`USERPROFILES_USE_PROFILE`
    If enabled, userprofiles will look for the model set in
    `AUTH_PROFILE_MODULE`.  it's likely that you need to overwrite
    `USERPROFILES_REGISTRATION_FORM` to add your additional profile fields and
    define a `save_profile` method which is called after the user was created.

`USERPROFILES_INLINE_PROFILE_ADMIN`
    If enabled, userprofiles will add a profile inline to you user admin.


userprofiles.contrib.profiles
------------------------------

django-userprofiles also comes with a contrib app to allow profile changes and
a profile view.

`USERPROFILES_PROFILE_FORM`
    You can overwrite the default profile form to add extra functionality.
    The default form is a ModelForm for you AUTH_PROFILE_MODULE.

`USERPROFILES_PROFILE_ALLOW_EMAIL_CHANGE`
    If enabled, the user is allowed to simply change the email address in the
    profile change view. This setting can only be activated if
    `USERPROFILES_CHECK_UNIQUE_EMAIL` is disabled.

    If you want to check for unique emails and allow your users to change
    their email addresses, you have to use the emailverification app.

`USERPROFILES_PROFILE_CHANGE_DONE_URL`
    Defines the redirect destination after the profile was saved. Defaults to
    the named URL `userprofiles_profile_change`.


userprofiles.contrib.emailverification
--------------------------------------

django-userprofiles provides a simple app to do confirmed email address changes.
(Users have the re-verify their email address after a change)

`USERPROFILES_EMAIL_VERIFICATION_DAYS`
    Defines the number of days a user has time to verify her/his new email
    address.  Defaults to 2.

`USERPROFILES_EMAIL_VERIFICATION_DONE_URL`
    Defines the redirect destination after the email change was verified.
    Defaults to the named URL `userprofiles_email_change`.


Tools
-----

There is an auth backend which allows your users to log in using their email
address.  Add `userprofiles.auth_backends.EmailOrUsernameModelBackend` to your
settings if you want to use this feature.


Kudos to (the people who inspired me to write this code)
--------------------------------------------------------

- django-registration by James Bennett
  (https://bitbucket.org/ubernostrum/django-registration/)

- to be continued..
  If I used your code, send me a message! I'll add you to this list.

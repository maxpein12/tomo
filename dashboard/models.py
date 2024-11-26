from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.hashers import check_password

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name
    


class Client(models.Model):
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    email = models.EmailField()
    profile_pic = models.CharField(max_length=100, default='')
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.name} {self.email} {self.gender}'
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    piece = models.IntegerField()
    # image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name
    

class Orders(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=100)
    quantity = models.IntegerField(8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
    
class AdminInquiry(models.Model):
    pkadmin_inquiry = models.BigAutoField(primary_key=True)
    message = models.TextField(blank=True, null=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_inquiry'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlockUser(models.Model):
    pkid = models.BigAutoField(primary_key=True)
    user_from = models.BigIntegerField(blank=True, null=True)
    user_to = models.BigIntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'block_user'


class BoardCategory(models.Model):
    pkcategory = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board_category'


class BoardPosts(models.Model):
    pkboardpost = models.BigAutoField(primary_key=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board_posts'


class Boards(models.Model):
    pkboard = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    fkcategory = models.ForeignKey(BoardCategory, models.DO_NOTHING, db_column='fkcategory', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boards'


class Configuration(models.Model):
    pkconfiguration = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=126)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configuration'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inquiries(models.Model):
    pkinquiry = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    subject = models.CharField(max_length=128, blank=True, null=True)
    message = models.TextField()
    is_read = models.IntegerField()
    parent_pkinquiry = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'inquiries'


class Match(models.Model):
    pkmatch = models.BigAutoField(primary_key=True)
    user_from = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_from', blank=True, null=True)
    user_to = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_to', related_name='match_user_to_set', blank=True, null=True)
    matched = models.IntegerField(blank=True, null=True)
    date_time = models.CharField(max_length=50, blank=True, null=True)
    accepted = models.IntegerField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    seen = models.IntegerField(blank=True, null=True)
    new = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match'


class MessageTemplates(models.Model):
    pkmessage_template = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'message_templates'


class Messages(models.Model):
    pkmessage = models.BigAutoField(primary_key=True)
    msg_from = models.ForeignKey('Users', models.DO_NOTHING, db_column='msg_from', blank=True, null=True)
    msg_to = models.ForeignKey('Users', models.DO_NOTHING, db_column='msg_to', related_name='messages_msg_to_set', blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, db_collation='utf16_unicode_ci', blank=True, null=True)
    datetime = models.CharField(max_length=50, db_collation='utf16_unicode_ci', blank=True, null=True)
    timezone = models.CharField(max_length=50, db_collation='utf16_unicode_ci', blank=True, null=True)
    read = models.IntegerField(blank=True, null=True)
    save = models.IntegerField(blank=True, null=True)
    callstatus = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messages'


class Photos(models.Model):
    pkphoto = models.BigAutoField(primary_key=True)
    photo = models.TextField(blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photos'


class Points(models.Model):
    pkpoint = models.BigAutoField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)
    datetime = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'points'


class PointsBundle(models.Model):
    pkpoint_bundle = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=True, null=True)
    percentage = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promo_percentage = models.CharField(max_length=50, blank=True, null=True)
    name = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    description = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    sku = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    call_minutes = models.IntegerField(blank=True, null=True)
    mail_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'points_bundle'


class PostComments(models.Model):
    pkpost_comment = models.BigAutoField(primary_key=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)
    comment = models.TextField(db_collation='utf8mb4_unicode_520_ci', blank=True, null=True)
    fkpost = models.BigIntegerField(blank=True, null=True)
    datetime = models.CharField(max_length=50, db_collation='utf16_unicode_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_comments'


class PostLikes(models.Model):
    pkpost_like = models.BigAutoField(primary_key=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)
    fkpost = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_likes'


class PostUnlikes(models.Model):
    pkpost_unlike = models.BigAutoField(primary_key=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)
    fkpost = models.ForeignKey('Posts', models.DO_NOTHING, db_column='fkpost', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_unlikes'


class Posts(models.Model):
    pkpost = models.BigAutoField(primary_key=True)
    fkboard = models.ForeignKey(Boards, models.DO_NOTHING, db_column='fkboard', blank=True, null=True)
    description = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)
    datetime = models.CharField(max_length=20, db_collation='utf16_unicode_ci', blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'

    def __str__(self):
        return f"Post {self.pkpost} by {self.fkuser.username}: {self.description}"


class Purchase(models.Model):
    pkpurchase = models.BigAutoField(primary_key=True)
    fkbundle = models.ForeignKey(PointsBundle, models.DO_NOTHING, db_column='fkbundle', blank=True, null=True)
    fkuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='fkuser', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase'


class UserUnlikes(models.Model):
    pkuser_unlike = models.BigAutoField(primary_key=True)
    user_from = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_from', blank=True, null=True)
    user_to = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_to', related_name='userunlikes_user_to_set', blank=True, null=True)
    datetime = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_unlikes'


class Users(models.Model):
    pkuser = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    password = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    firstname = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    middlename = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    lastname = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    about = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    job_title = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    company = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    school = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    location = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    remember_token = models.CharField(max_length=128, db_collation='utf16_unicode_ci', blank=True, null=True)
    email = models.CharField(max_length=128, db_collation='utf16_unicode_ci', blank=True, null=True)
    region = models.CharField(max_length=128, db_collation='utf16_unicode_ci', blank=True, null=True)
    fb_linked = models.IntegerField(blank=True, null=True)
    ig_linked = models.IntegerField(blank=True, null=True)
    fb_account_id = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    phone_number = models.CharField(max_length=50, db_collation='utf16_unicode_ci', blank=True, null=True)
    socket_id = models.CharField(max_length=50, db_collation='utf16_unicode_ci', blank=True, null=True)
    salt = models.CharField(max_length=10, db_collation='utf16_unicode_ci', blank=True, null=True)
    latitude = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    longitude = models.CharField(max_length=100, db_collation='utf16_unicode_ci', blank=True, null=True)
    nickname = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    gender_preference = models.IntegerField(blank=True, null=True)
    distancethreshold = models.CharField(db_column='distanceThreshold', max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    role_id = models.IntegerField()
    # audio_call_step = models.IntegerField(blank=True, null=True)
    age_verified = models.IntegerField(blank=True, null=True)
    dummy_account = models.IntegerField(blank=True, null=True)
    marital_status = models.IntegerField(blank=True, null=True)
    presence_of_children = models.IntegerField(blank=True, null=True)
    marriage_desire = models.IntegerField(blank=True, null=True)
    like_children_or_not = models.IntegerField(blank=True, null=True)
    presence_of_pet = models.IntegerField(blank=True, null=True)
    smoker = models.IntegerField(blank=True, null=True)
    drink = models.IntegerField(blank=True, null=True)
    holiday = models.IntegerField(blank=True, null=True)
    hobbie = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    bloodtype = models.CharField(max_length=20, db_collation='utf16_unicode_ci', blank=True, null=True)
    flip_count = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    notify_updates = models.IntegerField(blank=True, null=True)
    character = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    introduction = models.TextField(db_collation='utf16_unicode_ci', blank=True, null=True)
    registration_datetime = models.CharField(max_length=120, blank=True, null=True)
    drop_calls = models.IntegerField(blank=True, null=True)
    notify_likes = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.PositiveIntegerField(blank=True, null=True)
    token = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    mail_count = models.IntegerField(blank=True, null=True)
    call_minutes = models.FloatField(blank=True, null=True)
    udid = models.CharField(max_length=128, db_collation='utf16_unicode_ci')
    push_token = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    # pushkittoken = models.CharField(max_length=255, db_collation='utf16_unicode_ci', blank=True, null=True)
    resetpasswordcode = models.CharField(max_length=45, db_collation='utf16_unicode_ci', blank=True, null=True)

    
    
    
    def check_password(self, password):
        return check_password(password, self.password)

    def get_password(self):
        return "*****"  # or any other placeholder you want to display

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name



class ViewedProfile(models.Model):
    pkprofile_view = models.BigAutoField(primary_key=True)
    fkviewer = models.BigIntegerField(blank=True, null=True)
    fkviewed_profile = models.BigIntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    liked = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viewed_profile'
# Generated by Django 5.1.3 on 2024-11-30 14:30

import django.core.validators
import django.utils.timezone
import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('major', models.CharField(max_length=15)),
                ('student_id', models.CharField(max_length=8, unique=True, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.MaxLengthValidator(8)])),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('cp_number', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(11)])),
                ('image', models.ImageField(default='default.png', upload_to='upload_filepath')),
                ('is_manager', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('solbaram', '솔바람'), ('souly', 'SoulLy'), ('unhyang', '운향'), ('unhyun', '운현극예술 연구회'), ('kadleya', '카들레아'), ('fork', 'F.O.R.K'), ('pice', 'P.I.C.E'), ('mods', 'M.O.D.s'), ('unsan', '운산'), ('flora', 'FC Flora'), ('highclear', '하이클리어'), ('beautifly', 'BEAUTIFLY'), ('windown', 'Win Hands Down'), ('issue', 'ISSUE'), ('yeoleum', '열음'), ('yeun', '예운'), ('unjimoon', '운지문학회'), ('hanbit', '한빛'), ('filmsopi', '필름소피'), ('doodling', '두들링'), ('lion', '멋쟁이 사자처럼'), ('duckbool', '덕불'), ('theresa', '데레사'), ('ccc', 'CCC'), ('radius', 'RADIUS'), ('fm419', 'FM419'), ('jasang', '자세히생각하라'), ('io', '이오'), ('rotaract', '덕성로타트랙'), ('kusa', 'KUSA'), ('dodam', '도담도담'), ('deoknyang', '덕냥당'), ('flowersin', '꽃신을 신고')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]

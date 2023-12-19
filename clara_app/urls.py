

from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='clara_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/urls.py)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_config/', views.user_config, name='user_config'),
    path('admin_password_reset/', views.admin_password_reset, name='admin_password_reset'),
    path('add_credit/', views.add_credit, name='add_credit'),
    path('credit_balance/', views.credit_balance, name='credit_balance'),
    path('view_task_updates/', views.view_task_updates, name='view_task_updates'),
    path('delete_tts_data/', views.delete_tts_data, name='delete_tts_data'),
    path('delete_tts_data_status/<str:report_id>/', views.delete_tts_data_status, name='delete_tts_data_status'),
    path('delete_tts_data_monitor/<str:language>/<str:report_id>/', views.delete_tts_data_monitor, name='delete_tts_data_monitor'),
    path('delete_tts_data_complete/<str:language>/<str:status>/', views.delete_tts_data_complete, name='delete_tts_data_complete'),
    path('manage_language_masters/', views.manage_language_masters, name='manage_language_masters'),
    path('remove_language_master/<int:pk>/', views.remove_language_master, name='remove_language_master'),
    path('edit_prompt/', views.edit_prompt, name='edit_prompt'),
    path('edit_phonetic_lexicon/', views.edit_phonetic_lexicon, name='edit_phonetic_lexicon'),
    path('register_content/', views.register_content, name='register_content'),
    path('content_success/', views.content_success, name='content_success'),
    path('content_list/', views.content_list, name='content_list'),
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),
    path('create_project/', views.create_project, name='create_project'),
    path('project_list/', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/manage_project_members/', views.manage_project_members, name='manage_project_members'),
    path('project/<int:permission_id>/remove_project_member/', views.remove_project_member, name='remove_project_member'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),  
    path('project/<int:project_id>/clone_project/', views.clone_project, name='clone_project'),
    path('project/<int:project_id>/audio_metadata/', views.get_audio_metadata_view, name='get_audio_metadata'),
    path('project/<int:project_id>/create_plain_text/', views.create_plain_text, name='create_plain_text'),
    path('project/<int:project_id>/create_summary/', views.create_summary, name='create_summary'),
    path('project/<int:project_id>/create_cefr_level/', views.create_cefr_level, name='create_cefr_level'),
    path('project/<int:project_id>/create_segmented_text/', views.create_segmented_text, name='create_segmented_text'),
    path('project/<int:project_id>/create_phonetic_text/', views.create_phonetic_text, name='create_phonetic_text'),
    path('project/<int:project_id>/create_glossed_text/', views.create_glossed_text, name='create_glossed_text'),
    path('project/<int:project_id>/create_lemma_tagged_text/', views.create_lemma_tagged_text, name='create_lemma_tagged_text'),
    path('project/<int:project_id>/create_lemma_and_gloss_tagged_text/', views.create_lemma_and_gloss_tagged_text, name='create_lemma_and_gloss_tagged_text'),
    path('project/<int:project_id>/history/', views.project_history, name='project_history'),
    path('project/<int:project_id>/human_audio_processing/', views.human_audio_processing, name='human_audio_processing'),
    path('project/<int:project_id>/human_audio_processing_phonetic/', views.human_audio_processing_phonetic, name='human_audio_processing_phonetic'),
    path('project/<int:project_id>/process_ldt_zipfile_status/<str:report_id>/', views.process_ldt_zipfile_status, name='process_ldt_zipfile_status'),
    path('project/<int:project_id>/process_ldt_zipfile_monitor/<str:report_id>/', views.process_ldt_zipfile_monitor, name='process_ldt_zipfile_monitor'),
    path('project/<int:project_id>/process_ldt_zipfile_complete/<str:status>/', views.process_ldt_zipfile_complete, name='process_ldt_zipfile_complete'),
    path('project/<int:project_id>/generate_audio_metadata/<str:metadata_type>/<str:human_voice_id>/', views.generate_audio_metadata, name='generate_audio_metadata'),
    path('project/<int:project_id>/generate_audio_metadata_phonetic/<str:metadata_type>/<str:human_voice_id>/', views.generate_audio_metadata_phonetic, name='generate_audio_metadata_phonetic'),
    path('project/<int:project_id>/process_manual_alignment_status/<str:report_id>/', views.process_manual_alignment_status, name='process_manual_alignment_status'),
    path('project/<int:project_id>/process_manual_alignment_monitor/<str:report_id>/', views.process_manual_alignment_monitor, name='process_manual_alignment_monitor'),
    path('project/<int:project_id>/process_manual_alignment_complete/<str:status>/', views.process_manual_alignment_complete, name='process_manual_alignment_complete'),
    path('project/<int:project_id>/generate_annotated_segmented_file/', views.generate_annotated_segmented_file, name='generate_annotated_segmented_file'),
    path('project/<int:project_id>/edit_images/', views.edit_images, name='edit_images'),
    path('project/<int:project_id>/render_text_start_normal/', views.render_text_start_normal, name='render_text_start_normal'),
    path('project/<int:project_id>/render_text_start_phonetic/', views.render_text_start_phonetic, name='render_text_start_phonetic'),
    path('project/<int:project_id>/render_text_status/<str:report_id>/', views.render_text_status, name='render_text_status'),
    path('project/<int:project_id>/render_text_monitor/<str:phonetic_or_normal>/<str:report_id>/', views.render_text_monitor, name='render_text_monitor'),
    path('project/<int:project_id>/render_text_complete/<str:phonetic_or_normal>/<str:status>/', views.render_text_complete, name='render_text_complete'),
    path('project/<int:project_id>/make_export_zipfile/', views.make_export_zipfile, name='make_export_zipfile'),
    path('project/<int:project_id>/make_export_zipfile_status/<str:report_id>/', views.make_export_zipfile_status, name='make_export_zipfile_status'),
    path('project/<int:project_id>/make_export_zipfile_monitor/<str:report_id>/', views.make_export_zipfile_monitor, name='make_export_zipfile_monitor'),
    path('project/<int:project_id>/make_export_zipfile_complete/<str:status>/', views.make_export_zipfile_complete, name='make_export_zipfile_complete'), 
    path('project/<int:project_id>/offer_to_register_content_normal/', views.offer_to_register_content_normal, name='offer_to_register_content_normal'),
    path('project/<int:project_id>/offer_to_register_content_phonetic/', views.offer_to_register_content_phonetic, name='offer_to_register_content_phonetic'),
    path('project/<int:project_id>/register_project_content/<str:phonetic_or_normal>/', views.register_project_content, name='register_project_content'),
    path('project/<int:project_id>/generate_text_status/<str:report_id>/', views.generate_text_status, name='generate_text_status'),
    path('project/<int:project_id>/generate_text_monitor/<str:version>/<str:report_id>/', views.generate_text_monitor, name='generate_text_monitor'),
    path('project/<int:project_id>/generate_text_complete/<str:version>/<str:status>/', views.generate_text_complete, name='generate_text_complete'),
    path('projects/<int:project_id>/compare_versions/', views.compare_versions, name='compare_versions'),
    path('projects/<int:project_id>/metadata/<str:version>/', views.get_metadata_for_version, name='get_metadata_for_version'),
    path('rendered_texts/<int:project_id>/<str:phonetic_or_normal>/static/<path:filename>', views.serve_rendered_text_static, name='serve_rendered_text'),
    path('rendered_texts/<int:project_id>/<str:phonetic_or_normal>/multimedia/<path:filename>', views.serve_rendered_text_multimedia, name='serve_rendered_text'),
    path('rendered_texts/<int:project_id>/<str:phonetic_or_normal>/<path:filename>', views.serve_rendered_text, name='serve_rendered_text'),
    path('serve_zipfile/<int:project_id>/', views.serve_zipfile, name='serve_zipfile'),
    path('serve_export_zipfile/<int:project_id>/', views.serve_export_zipfile, name='serve_export_zipfile'),
    path('projects/serve_project_image/<str:project_id>/<path:base_filename>', views.serve_project_image, name='serve_project_image'),
    path('serve_audio_file/<str:engine_id>/<str:l2>/<str:voice_id>/<str:base_filename>', views.serve_audio_file, name='serve_audio_file'),

    path('manual_audio_alignment_integration_endpoint1/<int:project_id>/', views.manual_audio_alignment_integration_endpoint1, name='manual_audio_alignment_integration_endpoint1'),
    path('manual_audio_alignment_integration_endpoint2/', views.manual_audio_alignment_integration_endpoint2, name='manual_audio_alignment_integration_endpoint2'),

]


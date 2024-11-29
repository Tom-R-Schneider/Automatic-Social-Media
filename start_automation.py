import os
import sys

sys.path.append(os.getcwd())

import create_content.create_data as create_data
import create_content.create_content as create_content
import social_media.upload_posts as upload_post


create_data.start_create_data()
create_content.start_content_creation_process()
# upload_post.start_upload_process()
from app import db, create_app
from app.models import User

import schedule
import time

from datetime import datetime


# app = create_app(config_name='production')
#
# def job():
#     with app.app_context():
#         day_filter = datetime.utcnow()
#         try:
#             expired = db.session.query(User).filter(User.is_confirmed == False).filter(
#                 User.expire < day_filter).delete()
#             db.session.commit()
#             print('The cron job scheduled every hour deleted {} users'.format(expired))
#         except:
#             db.session.rollback()
#         finally:
#             db.session.close()
#
# schedule.every(1).minutes.do(job)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)
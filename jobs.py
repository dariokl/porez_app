from app import db, create_app
from app.models import User

from datetime import datetime

app = create_app(config_name='production')
with app.app_context():
    day_filter = datetime.utcnow()
    try:
        expired = db.session.query(User).filter(User.is_confirmed == False).filter(User.expire < day_filter).delete()
        db.session.commit()
        print('The cron job scheduled every hour deleted {} users'.format(expired))
    except:
        db.session.rollback()
    finally:
        db.session.close()
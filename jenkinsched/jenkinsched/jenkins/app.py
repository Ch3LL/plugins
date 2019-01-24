import datetime


class Jenkins(object):

    uri = '/jenkins'

    def get(self):
        user = __user__.query.filter_by(jenkins=True).first()
        if not user:
            user = __user__.query.order_by(__user__.order).first()
            user.jenkins = True
            __db__.session.commit()
        return __flask__.jsonify({
            'jenkins': user.name,
            'date': user.date.strftime('%A, %B %d, %Y')
        })

    def put(self):
        users = __user__.query.order_by(__user__.order).all()
        nextuser = False
        for user in users:
            if user.jenkins is True:
                user.jenkins = False
                __db__.session.commit()
                nextuser = True
            elif user.enabled == 0:
                continue
            elif nextuser is True:
                user.jenkins = True
                user.date = datetime.datetime.now()
                __db__.session.commit()
                nextuser = False
                ret = {'nextjenkins': user.name, 'date': user.date.strftime('%A, %B %d, %Y')}
                break
        if nextuser is True:
            for user in users:
                if user.enabled == 1:
                    user.jenkins = True
                    user.date = datetime.datetime.now()
                    __db__.session.commit()
                    ret = {'nextjenkins': user.name, 'date': user.date.strftime('%A, %B %d, %Y')}
                    break
        return __flask__.jsonify(ret)

import http.client
from flask_restx import Namespace, Resource
from wh.models import BeerModel
from wh.db import db

admin_namespace = Namespace('admin', description='Admin operations')


@admin_namespace.route('/beers/<int:beer_id>/')
class BeersDelete(Resource):

    @admin_namespace.doc('delete_beer',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, beer_id):
        '''
        Delete a beer
        '''
        beer = BeerModel.query.get(beer_id)
        if not beer:
            # The beer is not present
            return '', http.client.NO_CONTENT

        db.session.delete(beer)
        db.session.commit()

        return '', http.client.NO_CONTENT

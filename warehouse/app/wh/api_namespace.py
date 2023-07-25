import http.client
from datetime import datetime
from flask_restx import Namespace, Resource, fields
from wh import config
from wh.models import BeerModel
from wh.token_validation import validate_token_header
from wh.db import db
from flask import abort

api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username


# Input and output formats for Beer

authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

name_parser = authentication_parser.copy()
name_parser.add_argument('name', type=str,
                         required=True, help='name of the beer')

search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                           help='Search beers by name')

model = {
    'id': fields.Integer(),
    'name': fields.String(),
    'timestamp': fields.DateTime(),
}
beer_model = api_namespace.model('Beer', model)


@api_namespace.route('/beers/')
class BeersListCreate(Resource):

    @api_namespace.doc('list_beers')
    @api_namespace.expect(search_parser)
    @api_namespace.marshal_with(beer_model, as_list=True)
    def get(self):
        '''
        Retrieves all the beers
        '''
        args = search_parser.parse_args()
        search_param = args['search']
        query = BeerModel.query
        if search_param:
            query = (query.filter(BeerModel.name.contains(search_param)))

        query = query.order_by('id')
        beers = query.all()

        return beers

    @api_namespace.doc('create_beer')
    @api_namespace.expect(name_parser)
    @api_namespace.marshal_with(beer_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new beer
        '''
        args = name_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])
        print(">>>", username)

        new_beer = BeerModel(name=args['name'],
                             timestamp=datetime.utcnow())
        db.session.add(new_beer)
        db.session.commit()

        result = api_namespace.marshal(new_beer, beer_model)

        return result, http.client.CREATED


@api_namespace.route('/beers/<int:beer_id>/')
class BeersRetrieve(Resource):

    @api_namespace.doc('retrieve_beer')
    @api_namespace.marshal_with(beer_model)
    def get(self, beer_id):
        '''
        Retrieve a thought
        '''
        beer = BeerModel.query.get(beer_id)
        if not beer:
            # The beer is not present
            return '', http.client.NOT_FOUND

        return beer

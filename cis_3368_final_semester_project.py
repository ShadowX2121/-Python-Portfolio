import flask # *Referenced from class files, and Homework 2.*
import mysql.connector # *Referenced from class files, Homework 1, and Homework 2.*

from flask import jsonify # *Referenced from class files, and Homework 2.*
from flask import request # *Referenced from class files, and Homework 2.*

'''
This function establishes a connection to the specific MySQL database that is to be worked in.
*Referenced from class files, Homework 1, and Homework 2.*
'''
def create_database_connection():
    connection = None
    connection = mysql.connector.connect(
        host = 'aacis3368summer2024.(##########).(region).(database hosting service)', # Endpoint address for the database that MySQL connects to and manages (currently filled will null information).
        user = 'admin',
        password = '############', # Password for the admin account that has full admin privileges to the database that MySQL is connected to (currently filled with null information).
        database = 'aacis3368summerdb'
    )
    return connection

'''
This function is responsible for executing MySQL statements that make changes to the data within the MySQL database.
*Referenced from class files, Homework 1, and Homework 2.*
'''
def execute_query(database_connection, sql_query):
    database_cursor = database_connection.cursor()
    database_cursor.execute(sql_query)
    database_connection.commit()

'''
This function is responsible for executing MySQL statements that reads the data within the MySQL database and formatting it, so it can be displayed
in json format.
*Referenced from class files, Homework 1, and Homework 2.*
'''
def execute_read_query(database_connection, sql_query):
    database_cursor = database_connection.cursor(dictionary = True)
    database_table_rows = None
    database_cursor.execute(sql_query)
    database_table_rows = database_cursor.fetchall()
    return database_table_rows


sql_database_app = flask.Flask(__name__) # *Referenced from class files, and Homework 2.*

'''
This api route uses the GET method to display all of the data in the captain table in the MySQL database, and returns them in 
json format.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/captain', methods=['GET'])
def captain_read_all():
    database_connection = create_database_connection()
    mysql_get_statement = 'select * from captain'
    captain_table = execute_read_query(database_connection, mysql_get_statement)
    return jsonify(captain_table)

'''
This api route uses the GET method to display all of the data in the spaceship table in the MySQL database, and returns them in 
json format.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/spaceship', methods=['GET'])
def spaceship_read_all():
    database_connection = create_database_connection()
    mysql_get_statement = 'select * from spaceship'
    spaceship_table = execute_read_query(database_connection, mysql_get_statement)
    return spaceship_table

'''
This api route uses the GET method to display all of the data in the cargo table in the MySQL database, and returns them in 
json format.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/cargo', methods=['GET'])
def cargo_read_all():
    database_connection = create_database_connection()
    mysql_get_statement = 'select * from cargo'
    cargo_table = execute_read_query(database_connection, mysql_get_statement)
    return jsonify(cargo_table)

'''
This api route uses the POST method to add information about a new captain into the captain table of the MySQL database by receiving json formatted data and
using it in a MySQL statement to add it as a new row in the captain table and then displays a success message.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/captain', methods=['POST'])
def add_new_captain_entry():
    request_new_information = request.get_json()
    new_first_name = request_new_information['firstname']
    new_last_name = request_new_information['lastname']
    new_organization_rank = request_new_information['rank']
    new_homeplanet = request_new_information['homeplanet']
    database_connection = create_database_connection()
    mysql_add_statement = 'insert into captain(firstname, lastname, `rank`, homeplanet) values ("%s", "%s", "%s", "%s")' % (new_first_name, new_last_name, new_organization_rank, new_homeplanet)
    execute_query(database_connection, mysql_add_statement)
    return "New captain sucessfully added!"

'''
This api route uses the POST method to add information about a new spaceship into the spaceship table of the MySQL database by receiving json formatted data using a MySQL read statement
to read the information in the captain table and searches it for the id of the captain for that spaceship by using an if statement contained within a for loop, if the id for the 
captain is found within the captain table then the new spaceship is added with its information received in json format by using it in a MySQL statement to add the information 
for that particular spaceship in the spaceship table but if the id of the captain isn't found within the captain table then an error message is displayed.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/spaceship', methods=['POST'])
def add_new_spaceship_entry():
    request_new_information = request.get_json()
    new_max_weight = request_new_information['maxweight']
    new_captain_id = request_new_information['captainid']
    
    database_connection = create_database_connection()
    captain_check_statement = 'select * from captain where id = %s' % (new_captain_id)
    captain_exists = execute_read_query(database_connection, captain_check_statement)
    
    if not captain_exists:
        return "Unable to add spaceship: Specified captain does not exist!"
    
    mysql_add_statement = 'insert into spaceship(maxweight, captainid) values ("%s", "%s")' % (new_max_weight, new_captain_id)
    execute_query(database_connection, mysql_add_statement)
    return "New spaceship successfully added!"
        
'''
This api route uses the POST method to add information about a new cargo into the cargo table of the MySQL database by receiving json formatted data and
using it in a MySQL statement to add it as a new row in the cargo table, only if the new cargo doesn't cause the total weight of the cargo on that particular
spaceship to exceed the maximum weight that spaceship can carry, and then displays a success message.
*Referenced from class files, Homework 2, and some example code provided from a ChatGPT prompt asking how to only allow new cargo to be
added to a spaceship that exists in the spaceship table, and doesn't cause the total weight of all the cargo on that spaceship to exceed the maximum weight that 
spaceship can carry.*
'''
@sql_database_app.route('/api/cargo', methods=['POST'])
def add_new_cargo_entry():
    request_new_information = request.get_json()
    new_cargo_weight = int(request_new_information['weight'])
    new_cargo_type = request_new_information['cargotype']
    new_ship_id = request_new_information['shipid']
    database_connection = create_database_connection()
    spaceship_check_statement = 'select * from spaceship where id = %s' % (new_ship_id)
    spaceship_result = execute_read_query(database_connection, spaceship_check_statement)
    if not spaceship_result:
        return "Unable to add cargo: Specified spaceship does not exist!"

    max_weight = spaceship_result[0]['maxweight']
    cargo_check_statement = 'select sum(weight) as total_weight from cargo where shipid = %s' % (new_ship_id)
    cargo_result = execute_read_query(database_connection, cargo_check_statement)
    current_total_weight = cargo_result[0]['total_weight'] or 0
    if (current_total_weight + new_cargo_weight) > max_weight:
        return "Unable to add cargo: Adding this cargo would exceed the spaceship's maximum weight!"
    
    mysql_add_statement = 'insert into cargo(weight, cargotype, shipid) values ("%s", "%s", "%s")' % (new_cargo_weight, new_cargo_type, new_ship_id)
    execute_query(database_connection, mysql_add_statement)
    return "New cargo successfully added!"
 
'''
This api route uses the DELETE method to delete the captain information associated with a specific id in the captain table of the MySQL database by 
receiving the id of the captain to be deleted in json format and using it in a MySQL statement to delete the associated row from the captain table
and then displays a success message.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/captain', methods=['DELETE'])
def erase_specific_captain_entry():
    request_id_to_be_deleted = request.get_json()
    id_of_captain_to_delete = request_id_to_be_deleted['id']
    database_connection = create_database_connection()
    mysql_delete_statement = 'delete from captain where id = %s' % (id_of_captain_to_delete)
    execute_query(database_connection, mysql_delete_statement)
    return "Sucessfully deleted the specified captain!"

'''
This api route uses the DELETE method to delete the spaceship information associated with a specific id in the spaceship table of the MySQL database by 
receiving the id of the spaceship to be deleted in json format and using it in a MySQL statement to delete the associated row from the spaceship table
and then displays a success message.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/spaceship', methods=['DELETE'])
def erase_specific_spaceship_entry():
    request_id_to_be_deleted = request.get_json()
    id_of_spaceship_to_delete = request_id_to_be_deleted['id']
    database_connection = create_database_connection()
    mysql_delete_statement = 'delete from spaceship where id = %s' % (id_of_spaceship_to_delete)
    execute_query(database_connection, mysql_delete_statement)
    return "Sucessfully deleted the specified spaceship!"

'''
This api route uses the DELETE method to delete the cargo information associated with a specific id in the cargo table of the MySQL database by 
receiving the id of the cargo to be deleted in json format and using it in a MySQL statement to delete the associated row from the cargo table
and then displays a success message.
*Referenced from class files, and Homework 2.*
'''
@sql_database_app.route('/api/cargo', methods=['DELETE'])
def erase_specific_cargo_entry():
    request_id_to_be_deleted = request.get_json()
    id_of_cargo_to_delete = request_id_to_be_deleted['id']
    database_connection = create_database_connection()
    mysql_delete_statement = 'delete from cargo where id = %s' % (id_of_cargo_to_delete)
    execute_query(database_connection, mysql_delete_statement)
    return "Sucessfully deleted the specified cargo!"

'''
This api route uses the PUT method to update the information of a specific captain, using its unique id, by receiving the id of the captain to be updated as part
of the url and updates it with the new information received in json format and using it in a MySQL statement to update the information for that particular captain in the
captain table and then displays a success message.
*Referenced from Homework 2.*
'''
@sql_database_app.route('/api/captain', methods=['PUT'])
def update_specific_captain_entry():
    if 'id' in request.args:
        id = int(request.args['id'])
        request_captain_data = request.get_json()
        updated_first_name = request_captain_data['firstname']
        updated_last_name = request_captain_data['lastname']
        updated_organization_rank = request_captain_data['rank']
        updated_homeplanet = request_captain_data['homeplanet']
        database_connection = create_database_connection()
        mysql_update_statement = 'update captain set firstname = "%s", lastname = "%s", `rank` = "%s", homeplanet = "%s" where id = %s' % (updated_first_name, updated_last_name, updated_organization_rank, updated_homeplanet, id)
        execute_query(database_connection, mysql_update_statement)
        return "Sucessfully updated the specified captain!"
    
'''
This api route uses the PUT method to update the information of a specific spaceship, using its unique id, by receiving the id of the spaceship to be updated as part
of the url, using a MySQL read statement to read the information in the captain table and searches it for the id of the new captain for that spaceship by using an if 
statement contained within a for loop, if the id for the new captain is found within the captain table then the specified spaceship is updated with the new information
received in json format by using it in a MySQL statement to update the information for that particular spaceship in the spaceship table but if the id of new captain isn't
found within the captain table then an error message is displayed.
*Referenced from Homework 2, and some example code provided from a ChatGPT prompt asking how to only allow the information of a particular spaceship to be updated if the captainid
matches the id of a captain that exists in the captain table.*
'''
@sql_database_app.route('/api/spaceship', methods=['PUT'])
def update_specific_spaceship_entry():
    if 'id' in request.args:
        id = int(request.args['id'])
        request_spaceship_data = request.get_json()
        updated_max_weight = request_spaceship_data['maxweight']
        updated_captain_id = request_spaceship_data['captainid']
        database_connection = create_database_connection()
        captain_check_statement = 'select * from captain where id = %s' % (updated_captain_id)
        captain_exists = execute_read_query(database_connection, captain_check_statement)
        
        if not captain_exists:
            return "Unable to update spaceship: Specified captain does not exist!"
        
        mysql_update_statement = 'update spaceship set maxweight = "%s", captainid = "%s" where id = %s' % (updated_max_weight, updated_captain_id, id)
        execute_query(database_connection, mysql_update_statement)
        return "Successfully updated the information of specified spaceship!"
    
'''
This api route uses the PUT method to update the departure date of a specific cargo, using its unique id, by receiving the id of the cargo to be updated as part
of the url and updates it with the new departure date received in json format and using it in a MySQL statement to update the departure date for that particular cargo in the
cargo table and then displays a success message.
*Referenced from Homework 2.*
'''
@sql_database_app.route('/api/cargo/departure', methods=['PUT'])
def update_specific_cargo_departure():
    if 'id' in request.args:
        id = int(request.args['id'])
        request_cargo_data = request.get_json()
        updated_departure_date = request_cargo_data['departure']
        database_connection = create_database_connection()
        mysql_update_statement = 'update cargo set departure = "%s" where id = %s' % (updated_departure_date, id)
        execute_query(database_connection, mysql_update_statement)
        return "Sucessfully updated the departure date for the specified cargo!"

'''
This api route uses the PUT method to update the arrival date of a specific cargo, using its unique id, by receiving the id of the cargo to be updated as part
of the url and updates it with the new arrival date received in json format and using it in a MySQL statement to update the arrival date for that particular cargo in the
cargo table and then displays a success message.
*Referenced from Homework 2.*
'''
@sql_database_app.route('/api/cargo/arrival', methods=['PUT'])
def update_specific_cargo_arrival():
    if 'id' in request.args:
        id = int(request.args['id'])
        request_cargo_data = request.get_json()
        updated_arrival_date = request_cargo_data['arrival']
        database_connection = create_database_connection()
        mysql_update_statement = 'update cargo set arrival = "%s" where id = %s' % (updated_arrival_date, id)
        execute_query(database_connection, mysql_update_statement)
        return "Sucessfully updated the arrival date for the specified cargo!"

'''
This api route uses the PUT method to update the weight and cargotype of a specific cargo, using its unique id, by receiving the id of the cargo to be updated as part
of the url and updates it with the new weight and cargotype, only if the shipid received matches a shipid of a spaceship that exists in the spaceship table and the updated weight
of the cargo doesn't cause the total weight of all the cargo on that spaceship to exceed the maximum weight that spaceship can carry, received in json format and using it in a MySQL
statement to update the weight and cargotype for that particular cargo in the cargo table and then displays a success message.
*Referenced from Homework 2 and some example code provided from a ChatGPT prompt asking how to only allow the information of a specific cargo to be updated if the shipid of a certain
spaceship exists, and if the updated weight of the cargo doesn't cause the updated total weight of all the cargo on that spaceship to exceed the spaceship's maximum weight.*
'''
@sql_database_app.route('/api/cargo', methods=['PUT'])
def update_specific_cargo_entry():
    if 'id' in request.args:
        id = int(request.args['id'])
        request_cargo_data = request.get_json()
        updated_cargo_weight = int(request_cargo_data['weight'])
        updated_cargo_type = request_cargo_data['cargotype']
        ship_id = request_cargo_data['shipid']
        database_connection = create_database_connection()
        current_cargo_statement = 'select weight from cargo where id = %s' % (id)
        current_cargo_result = execute_read_query(database_connection, current_cargo_statement)
        if not current_cargo_result:
            return "Unable to update cargo: Specified cargo does not exist!"

        current_cargo_weight = current_cargo_result[0]['weight']
        spaceship_statement = 'select maxweight from spaceship where id = %s' % (ship_id)
        spaceship_result = execute_read_query(database_connection, spaceship_statement)
        if not spaceship_result:
            return "Unable to update cargo: Associated spaceship does not exist!"

        max_weight = spaceship_result[0]['maxweight']
        total_cargo_weight_statement = 'select sum(weight) as total_weight from cargo where shipid = %s' % (ship_id)
        total_cargo_weight_result = execute_read_query(database_connection, total_cargo_weight_statement)
        current_total_weight = total_cargo_weight_result[0]['total_weight'] or 0
        new_total_weight = current_total_weight - current_cargo_weight + updated_cargo_weight
        if new_total_weight > max_weight:
            return "Unable to update cargo: The updated weight exceeds the spaceship's maximum weight!"

        mysql_update_statement = 'update cargo set weight = "%s", cargotype = "%s", shipid = "%s" where id = %s' % (updated_cargo_weight, updated_cargo_type, ship_id, id)
        execute_query(database_connection, mysql_update_statement)
        return "Successfully updated the weight and cargotype for the specified cargo!"


sql_database_app.run()
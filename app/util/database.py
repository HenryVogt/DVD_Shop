# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import psycopg2.extensions

import config

sql = {
    'default': 'SELECT %(cols)s FROM %(table)s ORDER BY %(sort_by)s %(sort_order)s LIMIT %%(limit)s OFFSET %%(offset)s',
    'default_count': 'SELECT COUNT(*) as count FROM %(table)s',
    'specific': 'SELECT %(cols)s FROM %(table)s WHERE %(key)s = %%(value)s',
    'search': 'SELECT %(cols)s FROM %(table)s WHERE %(kv_list)s ORDER BY %(sort_by)s %(sort_order)s LIMIT %%(limit)s OFFSET %%(offset)s',
    'search_count': 'SELECT COUNT(*) as count FROM %(table)s WHERE %(kv_list)s',

    'specific_products' : 'SELECT * FROM products_view WHERE %(where)s',
    'select_for_update' : 'SELECT * FROM %(table)s WHERE %(where)s FOR UPDATE',

    'update': 'UPDATE %(table)s SET %(kv_list)s WHERE %(key)s = %%(value)s',
    'insert' : 'INSERT INTO %(table)s (%(cols)s) VALUES (\'%(values)s\')',
    'insert_returning' : 'INSERT INTO %(table)s (%(cols)s) VALUES (\'%(values)s\') RETURNING %(returning)s'
}



class Database_wrapper(object):
    def __enter__(self):
        con_settings = {
            'host': config.DB_HOSTNAME,
            'dbname':   config.DB_NAME,
            'user':     config.DB_USER,
            'password': config.DB_PASSWORD
        }
        self.conn = psycopg2.connect(" ".join(["=".join([k,v]) for k,v in con_settings.items()]))
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def get_cursor(self):
        cursor = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cursor)
        return cursor

    def get_objects(self, db_info, block_size = 20, block_offset = 0, search_str = None, search_dict = None, sort_by = None, sort_order = 'ASC', count = False, precise = True):
        cursor = self.get_cursor()

        # wenn search_str gegeben, darf es keine praezise suche sein:
        if search_str:
            precise = False

        # String aus den gewuenschten Spaten machen
        cols = ", ".join(db_info['cols'])

        # Querystrings laden
        search_qstr = sql['search']
        default_qstr = sql['default']

        # Key-Value muster laden
        
        value_like_tpl = "%%%s%%"
        kv_compare_tpl = "%s = %%(%s)s"
        key_num_tpl = "%s"

        if not precise:
            # felder nicht cs vergleichen
            kv_compare_tpl = "%s ILIKE %%(%s)s "
            # alle Zahlen in text casten
            key_num_tpl = "CAST(%s as TEXT)"

        # Wenn kein sortby gegeben, nach key sortieren
        if not sort_by:
            sort_by = db_info['key']

        # wenn gezaehlt werden soll, entsprechende querystrings laden
        if count:
            search_qstr = sql['search_count']
            default_qstr = sql['default_count']

        # wenn es einen suchstring gibt, zaehlt dieser zuerst
        if search_str:
            search_strs = {}
            search_str_q_parts = []
            
            i = 0
            # Alle string parts abfragen ...
            for search_str_part in search_str.split(" "):
                search_strs['search_str_%s' % i] = value_like_tpl % search_str_part
                # OR-verknuepfte key-value liste basteln aus allen spalten
                search_str_q_parts.append(
                    ' OR '.join([
                        kv_compare_tpl % ((key_num_tpl % key) if db_info['cols'][key] != str else key, 'search_str_%s' % i) 
                        for key in db_info['cols']
                    ])
                )
                i += 1

            # ... und und-verknuepfen
            search_str_q = "(%s)" % ") AND (".join(search_str_q_parts)
            # Querystring fuer execute vorbereiten
            qstr = search_qstr % {'kv_list' : search_str_q , 'cols': cols, 'table': db_info['table'], 'sort_order': sort_order, 'sort_by' : sort_by}
            search_strs.update({'search_str': search_str, 'limit': block_size, 'offset': block_offset * block_size})
            cursor.execute(qstr, search_strs)

        elif search_dict:
            # AND-verknuepfte key-value liste basteln aus allen spalten, strings nicht case-sensitive abfragen
            kv_list = ' AND '.join([
        		kv_compare_tpl % ((key_num_tpl % key) if db_info['cols'][key] != str else key, key)
        	    for key in search_dict])

            qstr = search_qstr % {'kv_list' : kv_list, 'cols': cols, 'table': db_info['table'], 'sort_order': sort_order, 'sort_by' : sort_by}
            
	    value_dict = {}
            # wenn keine praezise suche, werte im search_dict fuer "LIKE" vorbereiten...
            if not precise:
                value_dict = {k: value_like_tpl % v for (k,v) in search_dict.items()}
	    else:
		value_dict = {k: v for (k,v) in search_dict.items()}
            # .. und um alle anderen felder erweitern
            value_dict.update({'limit': block_size, 'offset': block_offset * block_size})
            cursor.execute(qstr, value_dict)
 
        else:
            qstr = default_qstr % {'cols': cols, 'table': db_info['table'], 'sort_order': sort_order, 'sort_by' : sort_by}
            cursor.execute(qstr, {'limit': block_size, 'offset': block_offset * block_size})
        
        result = None
        if count:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        cursor.close()
        return result

    def get_object(self, db_info, key):
        cursor = self.get_cursor()
        qstr = sql['specific'] % {'cols': ", ".join(db_info['cols']), 'table': db_info['table'], 'key': db_info['key']}
        cursor.execute(qstr, {'value': key})
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_count(self, db_info, search_str = None, search_dict = None, precise = True):
        return self.get_objects(db_info = db_info, search_str = search_str, search_dict = search_dict, count = True, precise = precise)['count']
    
    def get_objects_forBasket(self, productList, db_info):
        cursor = self.get_cursor()

        where = ' OR '.join(['prod_id= %s' for prod_id in productList.keys()]) 
        qstr = sql['specific_products'] % {'where': where}
        cursor.execute(qstr, productList.keys())

        result = cursor.fetchall()
        cursor.close()
        return result

    def update_data(self, db_info, update_info, id):
        kv_compare_tpl = "%s = %%(%s)s"
        cursor = self.get_cursor()
        kv_list = ", ".join([kv_compare_tpl % (key, key) for key in update_info])
        qstr = sql['update'] % {'table': db_info['table'], 'key': db_info['key'], 'kv_list': kv_list}
        update_info['value'] = id
        try:
            cursor.execute(qstr, update_info)
        except Exception as ex:
            raise ex

    def update_data_inventory(self, db_info, update_info, id):
        kv_compare_tpl = "%s = %s"
        cursor = self.get_cursor()
        kv_list = ", ".join([kv_compare_tpl % (key, update_info[key]) for key in update_info.keys()])

        print kv_list

        qstr = sql['update'] % {'table': db_info['table'], 'key': db_info['key'], 'kv_list': kv_list}
        update_info['value'] = id
        try:
            cursor.execute(qstr, update_info)
        except Exception as ex:
            raise ex

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def select_for_update(self, db_info, productList):
        cursor = self.get_cursor()
        
        where = ' OR '.join(['prod_id= %s' for product in productList]) 
        qstr = sql['select_for_update'] % {'table': db_info['table'], 'where': where}
        cursor.execute(qstr, productList)

        result = cursor.fetchall()
        cursor.close()
        return result

    def insert(self, db_info, value_dic):
        cursor = self.get_cursor()
        values = []
        keys = []
        for key, value in value_dic.items():
            keys.append(key)
            values.append(str(value))

        if 'key' in db_info:
            qstr = sql['insert_returning'] % {'table':db_info['table'], 'cols' : ", ".join(keys), 'values': "', '".join(values), 'returning':db_info['key']}
        else:
            qstr = sql['insert'] % {'table':db_info['table'], 'cols' : ", ".join(keys), 'values': "', '".join(values)}

        cursor.execute(qstr, { })

        if 'key' in db_info:
            return cursor.fetchone()[db_info['key']]


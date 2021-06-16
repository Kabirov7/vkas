import psycopg2
import psycopg2.extras
from itemadapter import ItemAdapter


class VkasPipeline:
	def open_spider(self, spider):
		hostname = 'localhost'
		port = 5432
		username = 'postgres'
		password = 'postgres'
		database = 'one_time_use'

		self.connection = psycopg2.connect(host=hostname, user=username, password=password, port=port,
										   database=database, options=f'-c lock_timeout=0')
		self.cur = self.connection.cursor()

		self.cur.execute(
			"create table if not exists vkas (doc_num text, "
			"receipt_date varchar(30), "
			"info text, judje text, "
			"decision_date varchar(30), "
			"decision text, "
			"date_of_legal_force text, "
			"judical_acts text, "
			"judical_acts_url text);")
		self.connection.commit()

	def close_spider(self, spider):
		self.cur.close()
		self.connection.close()

	def process_item(self, item, spider):
		psycopg2.extras.execute_batch(self.cur, """INSERT INTO vkas(doc_num, 
								 receipt_date, 
								 info, 
								 judje, 
								 decision_date, 
								 decision, 
								 date_of_legal_force, 
								 judical_acts, 
								 judical_acts_url) 
						values (
						 		%(doc_num)s,
						 		%(receipt_date)s,
						 		%(info)s,
						 		%(judje)s,
						 		%(decision_date)s,
						 		%(decision)s,
						 		%(date_of_legal_force)s,
						 		%(judicial_acts)s,
						 		%(judicial_acts_url)s
						 ) """, [item], page_size=1000)
		self.connection.commit()
		print()

		return item

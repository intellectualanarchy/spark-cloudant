#*******************************************************************************
# Copyright (c) 2015 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#******************************************************************************/
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
import requests
import warnings

conf = SparkConf().setAppName("n_booking special char value predicate tests - Python")
conf.set("cloudant.host", "<cloudanthost>")
conf.set("cloudant.username", "<cloudantusername>")
conf.set("cloudant.password", "<cloudantpassword>")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def verifySpecCharValuePredicate():
	bookingData = sqlContext.sql("SELECT customerId, dateOfBooking FROM bookingTable1 WHERE customerId = 'uid0@email.com'")
	bookingData.printSchema()

	# verify expected count
	print ("bookingData.count() = ", bookingData.count())
	assert bookingData.count() == total_rows

	# verify customerId = 'uid0@email.com'
	for booking in bookingData.collect():
		assert booking.customerId == 'uid0@email.com'


# query the index using Cloudant API to get expected count
url = "https://<cloudanthost>/n_booking/_design/view/_search/n_bookings?q=customerId:uid0@email.com"
response = requests.get(url, auth=('<cloudantusername>', '<cloudantpassword>'))
assert response.status_code == 200
total_rows = response.json().get("total_rows")

# record a warning if there is no data to test, will check for 0 doc anyway
if total_rows == 0:
	warnings.warn("No data for uid0@email.com in the n_booking database!")


print ('About to test com.cloudant.spark for n_booking')
sqlContext.sql(" CREATE TEMPORARY TABLE bookingTable1 USING com.cloudant.spark OPTIONS ( database 'n_booking')")
verifySpecCharValuePredicate()

print ('About to test com.cloudant.spark.CloudantRP for n_booking')
sqlContext.sql(" CREATE TEMPORARY TABLE bookingTable1 USING com.cloudant.spark.CloudantPrunedFilteredRP OPTIONS ( database 'n_booking')")
verifySpecCharValuePredicate()

print ('About to test com.cloudant.spark.CloudantPrunedFilteredRP for n_booking')
sqlContext.sql(" CREATE TEMPORARY TABLE bookingTable1 USING com.cloudant.spark.CloudantPrunedFilteredRP OPTIONS ( database 'n_booking')")
verifySpecCharValuePredicate()

print ('About to test com.cloudant.spark.CloudantPartitionedPrunedFilteredRP for n_booking')
sqlContext.sql(" CREATE TEMPORARY TABLE bookingTable1 USING com.cloudant.spark.CloudantPartitionedPrunedFilteredRP OPTIONS ( database 'n_booking')")
verifySpecCharValuePredicate()
      

	


	
	

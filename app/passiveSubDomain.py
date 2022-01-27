from cgi import test
from sqlite3 import Timestamp
import requests
import threading
import whois
import confuse
import vt
import psycopg2 as db
import time
import datetime


def selectQuery(query):

    source = confuse.YamlSource('/home/burhan/projects/SubFinder/config.yaml')

    dataBaseConfig = source["database"]

    dbConnectionString = dataBaseConfig["dbConnectionString"]
        
    with db.connect(dbConnectionString) as connection:
        with connection.cursor() as cursor:

            cursor.execute(query)
            result = cursor.fetchall()

        return result

source = confuse.YamlSource('/home/burhan/projects/SubFinder/config.yaml')



def insertQuery(query):

    source = confuse.YamlSource('/home/burhan/projects/SubFinder/config.yaml')

    dataBaseConfig = source["database"]

    dbConnectionString = dataBaseConfig["dbConnectionString"]
        
    with db.connect(dbConnectionString) as connection:

        cursor = connection.cursor()
        cursor.execute(query)
            

    return "Success"


def subDomainCheck(url,domain,subDomainName):

    try:

        requests.get(url)
        print(f"{url} discoverd")
        query = f"call addSubDomain('{subDomainName}','{domain}')"
        insertQuery(query)

    except Exception as error:
        pass


def findSubDomain():

    domain = "google.com"

    subDomainFile = open(source["files"]["subDomainNames"],"r")

    subDomainNames = (subDomainFile.read()).splitlines()

    for subDomainName in subDomainNames:
        url  = f"http://{subDomainName}.{domain}"
        url1 = f"https://{subDomainName}.{domain}"

        threading.Thread(target=subDomainCheck, args=[url,domain,subDomainName]).start()
        threading.Thread(target=subDomainCheck, args=[url1,domain,subDomainName]).start()

        time.sleep(1)


def whoIs(url):

    whoIsInfos = whois.whois(url)  
    

    query = f"""
        call addWhoIsInfo(
            '{whoIsInfos.domain__id}',
            '{whoIsInfos.registrar}',
            '{whoIsInfos.registrar_id}',
            '{whoIsInfos.registrar_url}',
            '{replaceList(whoIsInfos.status)}',
            '{whoIsInfos.registrant_name}',
            '{whoIsInfos.registrant_state_province}',
            '{whoIsInfos.registrant_country}',
            '{replaceList(whoIsInfos.name_servers)}',
            '{(whoIsInfos.creation_date)[0]}',
            '{(whoIsInfos.expiration_date)[0]}',
            '{(whoIsInfos.updated_date)[0]}',
            '{url}'
        )
    """
    insertQuery(query)


def replaceList(value):
    return str(value).replace("['","").replace("']","").replace("'","").replace(",","") 



def virusTotalLastAnalysisStats(url):

    try:
        client = vt.Client(source["apikey"]["virustotal"])

        url_id = vt.url_id(url)

        url_id = client.get_object(f"/urls/{url_id}")

        lastAnalysisDate = url_id.last_analysis_date

        analysis = url_id.last_analysis_stats
        

        query = f"""
            call add_last_analysis_stats(
                {analysis['harmless']},
                {analysis["malicious"]},
                {analysis["suspicious"]},
                {analysis["undetected"]},
                {analysis["timeout"]},
                '{lastAnalysisDate}',
                '{url}'
            )
        """

        print(query)
        insertQuery(query)

    
    except Exception as error:
        print(f"Virus Total Last Analysis Stats = {error}","error")
    
    finally:
        client.close()




def virusTotal(url):

    try:

        client = vt.Client(source["apikey"]["virustotal"])

        url_id = vt.url_id(url)

        url_id = client.get_object(f"/urls/{url_id}")

        analysis = (url_id.last_analysis_results).values()

        test = f"select domainId from domainname where domainname = '{url}'"
    
        id = selectQuery(test)
        id = str(id).replace("[(","").replace(",)]","")
        print(id)

        for analys in analysis:
            
            query1 = f"""
            INSERT INTO last_analysis_results(
	        category, result, method, engine_name, urlid
            ) values (
                '{analys["category"]}',
                '{analys["result"]}',
                '{analys["method"]}',
                '{analys["engine_name"]}',
                {id}
            );	
            """
            print(query1)
            print("-------------------")
            insertQuery(query1)
    
    except Exception as error:
        print(f"Virus Total Last Analysis Result = {error}")

    finally:
        client.close()


def inetHostName(url):
    query = f"""
    select * 
      from whois
     where
        domainId = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """
    result = selectQuery(query)
    print(type(result))

    


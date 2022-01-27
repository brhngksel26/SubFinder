from re import template
from flask import Flask
from flask import request,jsonify,render_template
from threading import Thread
from app.databaseUtil import selectQueryFetchall,selectQueryFetchone

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/whois/<url>")
def whoIs(url):
    url = url + ".com"
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

    results = selectQueryFetchone(query)
    print(len(results))
    for result in results:
      print(result)

    return render_template('whois.html', results = results)


@app.route("/lastanaylisresults/<url>")
def lastAnaylisResults(url):
  url = url + ".com"
  query = f"""
    select * 
      from last_analysis_results
     where
        urlid = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """

  print(query)

  results = selectQueryFetchall(query)
  print(results)

  return render_template('lastanaylisresults.html', results = results)

@app.route("/lastanalysisstats/<url>")
def lastAnalysisStats(url):

  
  url = url + ".com"
  query = f"""
    select * 
      from last_analysis_stats
     where
        urlid = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """

  print(query)

  result = selectQueryFetchone(query)
  return render_template('lastanalysisstats.html', result = result,url=url)


@app.route("/subdomainname/<url>")
def subDomainName(url):
  
  url = url + ".com"
  query = f"""
    select * 
      from subdomainname
     where
        domainId = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """

  result = selectQueryFetchall(query)

  test = []
  for i in result:
    test.append(dict(i))

  print(test) 

  return render_template('subDomainName.html', results = result,url=url)



@app.route("/json/whois/<url>")
def whoIs2Json(url):
    url = url + ".com"
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

    results = selectQueryFetchone(query)
    print(len(results))
    for result in results:
      print(result)

    return jsonify({'result':results})


@app.route("/json/lastanaylisresults/<url>")
def lastAnaylisResults2Json(url):
  url = url + ".com"
  query = f"""
    select * 
      from last_analysis_results
     where
        urlid = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """

  print(query)

  result = selectQueryFetchall(query)
  print(result)

  return jsonify({'result':result})

@app.route("/json/lastanalysisstats/<url>")
def lastAnalysisStats2Json(url):

  
  url = url + ".com"
  query = f"""
    select * 
      from last_analysis_stats
     where
        urlid = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """

  print(query)

  result = selectQueryFetchone(query)
  return jsonify({'result':result})


@app.route("/json/subdomainname/<url>")
def subDomainName2Json(url):
  
  url = url + ".com"
  query = f"""
    select * 
      from subdomainname
     where
        domainId = 
               (
                   select domainId 
                     from domainname
                    where
                     domainname = '{url}'
                )
    """

  print(query)

  result = selectQueryFetchall(query)
  print(result)

  return jsonify({'result':result})
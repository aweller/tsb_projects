import urllib2

def main():
#     url = "https://dataloader.ionreporter.iontorrent.com:443/grws/sample/metadata?sampleName="
    url = "https://ir16.ionreporter.lifetechnologies.com/grws/rest/sample/metadata?sampleName="
#     url = "https://dataloader.ir16.ionreporter.lifetechnologies.com:443/grws/sample/metadata?sampleName="
    req = urllib2.Request(url)
    req.add_header("Authorization","xxxxxx")

    try:
        f = urllib2.urlopen(req)
        print f.read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[0]+" "+e.reason.args[1]
                
if __name__ == '__main__':
    main()

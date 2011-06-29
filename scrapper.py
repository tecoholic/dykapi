import urllib

import BeautifulSoup

def get_hook_data(url):
    ''' This Fucntion takes a "url" as input and returns a list of dictionaries
    The Dict is (text,link). Each Dict is a DYK hook. '''
    hooklist = []
    f = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(f.read())
    lis  = soup.findAll("li", attrs={"style":"-moz-float-edge: content-box"})
    for li in lis:
        try:
            link = li.b.a["href"]
        except TypeError:
            link = li.find("a")["href"]
        link = link.replace("/wiki/","")
        hook = { "text" : li.text, "link" : link }
        hooklist.append(hook)
    return hooklist

if __name__ == "__main__":
    data = get_hook_data("Wikipedia Recent_additions.htm")
    # data is a list of dictionaries
    print "--------------- Page Data: Properties -------------"
    print "\nNo of hooks: "+str(len(data))
    print "\nAvilable hook data: "+str(data[0].keys())
    print "\nSample Dict:\n"
    print data[0]

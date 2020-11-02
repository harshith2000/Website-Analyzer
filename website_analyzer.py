#import libraries
import bs4 as bs
import urllib.request
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import re
import pandas as pd
from pandas import DataFrame
from urllib.request import urlopen


#Given a URL, find the homepage of the website (sometimes you may be given a URL of an inner page)
def findhomepage(website):
    count=0
    homepage=""
    for i in website:
        if i=="/":
            count+=1
        if count!=3:    #the homepage will be present in the url before the 3rd '/' . eg: https:/(1/2www.exeterpremedia.com/3
            homepage+=i
        elif count==3:
            break
    return(homepage)


#Find the links in the home page (and remove duplicates)  &&  Store the links
def getandstorelinks(website):
    homepage=findhomepage(website)
    source = urllib.request.urlopen(website).read()
    soup = bs.BeautifulSoup(source,'lxml')
    links=[]
    for url in soup.find_all('a'):              #finding all anchor tags
        links.append(url.get('href'))        # getting all tags that have href
    d={}                                                #dictionary is created to remove duplicate links
    unique_links=[]
    for i in links:
        if i not in d:
            d[i]=1
            if i and i[0]=="h":                       #to remove unnecessary anchor tags and get only appropriate links i.e links starting with "https"
                unique_links.append(i)
    return(unique_links)


#For each link, get the web page, extract text and store it
def getwebpageandstoretext(website):
    homepage=findhomepage(website)
    unique_links=getandstorelinks(homepage)
    textineachlink=[]
    for eachlink in unique_links:
        if homepage in eachlink:
            source = urllib.request.urlopen(eachlink).read()
            soup = bs.BeautifulSoup(source,'lxml')
            textineachlink.append(soup.text)                                 #using soup.text to extract text from the webpage
    return textineachlink


#Parse the text (remove stop words, punctuation) and generate a list of uni-grams, and bi-grams from the text. We will refer to these as key terms.
def removepunctuationsandstopwords(website):  
    source = urllib.request.urlopen(website).read()
    soup = bs.BeautifulSoup(source,'lxml')
    sentence=soup.text
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(sentence) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)                                #remove stop words
    string=""
    for i in filtered_sentence:
        string=string+" "+i
    string = re.sub(r'[^\w\s]', '', string)                             #remove punctuations
    return string



#Function to generate unigrams
def uni_grams(sentence):
    dic={}
    unigram=[]
    sentence=sentence.split()
    return sentence

#Function to generate bigrams
def bi_grams(sentence):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    l = re.split(r' [\.\?!][\'"\)\]] *', sentence)
  #print(l)
  #return l
    if len(l[len(l)-1])==0:
        l.pop()
  #return l 
    ans=[]
    for i in l:
        kish=list(i.split())
        for j in range(1,len(kish)):
            str1=kish[j-1]
            str2=kish[j]
            tmp = ""
            for k in str1:
                if k not in punc and k!=' ' :
                    tmp += k
            str1=tmp.lower()
            tmp = ""
            for k in str2:
                if k not in punc and k!=' ' :
                    tmp += k
            str2=tmp.lower()
            ans.append(str1+" "+str2)
    return ans

#function to generate trigrams
def tri_grams(sentence):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    l = re.split(r' [\.\?!][\'"\)\]] *', sentence)
  #print(l)
  #return l
    if len(l[len(l)-1])==0:
        l.pop()
  #return l 
    ans=[]
    for i in l:
        kish=list(i.split())
        for j in range(2,len(kish)):
            str1=kish[j-2]
            str2=kish[j-1]
            str3=kish[j]
            tmp = ""
            for k in str1:
                if k not in punc and k!=' ' :
                    tmp += k
            str1=tmp.lower()
            tmp = ""
            for k in str2:
                if k not in punc and k!=' ' :
                    tmp += k
            str2=tmp.lower()
            tmp = ""
            for k in str3:
                if k not in punc and k!=' ' :
                    tmp += k
            str3=tmp.lower()
            ans.append(str1+" "+str2+" "+str3)
    return ans



# The number of top level pages (a top level page is  one that has a link on the home page)
def numberoftoplevelpages(website):
    homepage=findhomepage(website)
    unique_links=getandstorelinks(homepage)
    return(len(unique_links))


#Page titles of all the top level pages 
def topleveltitle(website):
    homepage=findhomepage(website)
    unique_links=getandstorelinks(homepage)
    titles=[]
    for i in unique_links:
        if homepage in i:
            source = urllib.request.urlopen(i).read()
            soup = bs.BeautifulSoup(source,'lxml')
            titles.append(soup.title)
    return titles


#Meta tags from all top level pages
def meta_tags(website):
    homepage=findhomepage(website)
    unique_links=getandstorelinks(homepage)
    metatags=[]
    for i in unique_links:
        if i and homepage in i:
            source = urllib.request.urlopen(i).read()
            soup = bs.BeautifulSoup(source,'lxml')
            metatags.append(soup.find('meta'))
    return metatags

#All internal links (links that point to some page in the same website)
def internal_links(website):
    homepage=findhomepage(website)
    unique_links=getandstorelinks(homepage)
    internallinks=[]
    for i in unique_links:
        if  i and homepage in i:             #checking whether the website name is in the link
            internallinks.append(i)
    return internallinks

#All external links (links that point to pages outside the site). 
def external_links(website):
    homepage=findhomepage(website)
    unique_links=getandstorelinks(homepage)
    externallinks=[]
    for i in unique_links:
        if  i and homepage not  in i:                 #checking whether the website name is not in the link
            externallinks.append(i)
    return externallinks    

#A frequency table of the top 20 key terms (unigrams and bigrams) in the descending order of frequency and write out a CSV file.
def findtop20(ngram):
    d={}
    top20=[]
    for i in ngram:
        if i not in d:
            d[i]=1
        else:
            d[i]+=1
    sorteddict = sorted(d, key=d.get, reverse=True)             #sorting the dictionary based on keys in descending order
    for i in range(20):
        top20.append(sorteddict[i])
    return top20

#Find the size of the web page
def findsizeofwebpage(website):
    r = urlopen(website)
    return len(r.read())

print('\033[1m' +"Enter the website URL")                          #'\033[1m' is used to print the text bold in python
website_name=input()
homepage_name=findhomepage(website_name)

linksinhomepage=[]
linksinhomepage=getandstorelinks(website_name)

textineachpage=getwebpageandstoretext(website_name)

clear_sentence=removepunctuationsandstopwords(website_name)
unigrams=uni_grams(clear_sentence)
bigrams=bi_grams(clear_sentence)
trigrams=tri_grams(clear_sentence)

number_of_top_level_pages=numberoftoplevelpages(website_name)

titles_list=topleveltitle(website_name)

meta_tags_list=meta_tags(website_name)



#printing the output in a csv file


df1=DataFrame({"Links in homepage":linksinhomepage})
df2=DataFrame({"Unigrams" : unigrams}) 
df3=DataFrame({"Bigrams" : bigrams})      
df4=DataFrame({"Trigrams" : trigrams})         
df5=DataFrame({"Page titles" :titles_list})
df6=DataFrame({"Meta tags" : meta_tags_list})
df7=DataFrame({"All internal links" : internal_links_list}) 
df8=DataFrame({"All external links" : external_links_list})

dffinal=final = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8],ignore_index = "False",axis=1)

dffinal.to_csv("output.csv",header=[ "Links in homepage" , "Unigrams" , "Bigrams" , "Trigrams" , "Page titles","Meta tags","All internal links" ,"All external links"])


internal_links_list=internal_links(website_name)

external_links_list=external_links(website_name)

top20unigrams=findtop20(unigrams)
top20bigrams=findtop20(bigrams)
top20trigrams=findtop20(trigrams)

sizeofwebpage=findsizeofwebpage(website_name)


#printing the output in a text file (output.txt)

print("INPUT SITE",file=open("output.txt", "a"))
print(website_name,file=open("output.txt", "a"))

print("\nHOME PAGE NAME",file=open("output.txt", "a"))
print(homepage_name,file=open("output.txt", "a"))

print("\nLINKS IN HOME PAGE",file=open("output.txt", "a"))
print(*linksinhomepage,sep="\n",file=open("output.txt", "a"))

# 1.The number of top level pages ((a top level page is  one that has a link on the home page)
print("\nNUMBER OF TOP LEVEL PAGES", file=open("output.txt", "a"))
print(number_of_top_level_pages, file=open("output.txt", "a"))

# 2.Page titles of all the top level pages 
print("\nPAGE TITLES OF ALL TOP LEVEL PAGES", file=open("output.txt", "a"))
print(*titles_list,sep="\n", file=open("output.txt", "a"))

# 3.Meta tags from all top level pages
print("\nMETA TAGS OF TOP LEVEL PAGES", file=open("output.txt", "a"))
print(*meta_tags_list,sep="\n", file=open("output.txt", "a"))

# 4. All internal links (links that point to some page in the same website) 
print("\nALL INTERNAL LINKS", file=open("output.txt", "a"))
print(*internal_links_list,sep="\n", file=open("output.txt", "a"))

# 5. All external links (links that point to pages outside the site).
print("\nALL EXTERNAL LINKS", file=open("output.txt", "a"))
print(*external_links_list,sep="\n", file=open("output.txt", "a"))


# 6. A frequency table of the top 20 key terms (unigrams and bigrams) in the descending order of frequency and write out a CSV file.
print("\nTOP 20 UNIGRAMS", file=open("output.txt", "a"))
print(*top20unigrams,sep="\n", file=open("output.txt", "a"))

print("\nTOP 20 BIGRAMS", file=open("output.txt", "a"))
print(*top20bigrams,sep="\n", file=open("output.txt", "a"))

print("\nTOP 20 TRIGRAMS", file=open("output.txt", "a"))
print(*top20trigrams,sep="\n", file=open("output.txt", "a"))

#frequency table in a csv file
top20dict={"TOP 20 UNIGRAMS" : top20unigrams, "TOP 20 BIGRAMS" : top20bigrams , "TOP 20 TRIGRAMS" : top20trigrams}
df1=pd.DataFrame(top20dict) 
df1.to_csv("top20ngrams.csv")

# Display the size of the webpage
print("\nSIZE OF WEB PAGE", file=open("output.txt", "a"))
print(str(sizeofwebpage/1024)+" kb", file=open("output.txt", "a"))



#printing the ouput in jupyter notebook


print('\033[1m' +"INPUT SITE")
print(website_name)

print('\033[1m' +"\nHOME PAGE NAME")
print(homepage_name)

print('\033[1m' +"\nLINKS IN HOME PAGE")
print(*linksinhomepage,sep="\n")

print('\033[1m' +"\nTEXT AFTER REMOVING PUNCTUATIONS AND STOP WORDS")
print(clear_sentence)

print('\033[1m' +"\nUNIGRAMS")
print(*unigrams,)

print('\033[1m' +"\nBIGRAMS")
print(*bigrams)

print('\033[1m' +"\nTRIGRAMS")
print(*trigrams)

print('\033[1m' +"\nNUMBER OF TOP LEVEL PAGES")
print(number_of_top_level_pages)

print('\033[1m' +"\nPAGE TITLES OF ALL TOP LEVEL PAGES")
print(*titles_list,sep="\n")

print('\033[1m' +"\nMETA TAGS OF TOP LEVEL PAGES")
print(*meta_tags_list,sep="\n")

print('\033[1m' +"\nALL INTERNAL LINKS")
print(*internal_links_list,sep="\n")

print('\033[1m' +"\nALL EXTERNAL LINKS")
print(*external_links_list,sep="\n")

print('\033[1m' +"\nTOP 20 UNIGRAMS")
print(*top20unigrams,sep="\n")

print('\033[1m' +"\nTOP 20 BIGRAMS")
print(*top20bigrams,sep="\n")

print('\033[1m' +"\nTOP 20 TRIGRAMS")
print(*top20trigrams,sep="\n")

print('\033[1m' +"\nSIZE OF WEB PAGE")
print(sizeofwebpage)







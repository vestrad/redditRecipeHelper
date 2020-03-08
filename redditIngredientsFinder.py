import requests
from bs4 import BeautifulSoup
import praw
import winsound
import time
def eraseUpTo(comment, KEYPHRASE):
    index = comment.find(KEYPHRASE)
    return comment[index:]
def findSentence(text):
    list = text.split()
    list.pop(0)
    result = " "
    result = result.join(list)
    #print(result)
    return result
def extractIngredientsType2(url):
    response = requests.get(url)
    results_page = BeautifulSoup(response.content, 'lxml')
    #try:
    if True:
        dictionary = {}
        ingredient_list = []
        directions = []
        page_list = results_page.find("section", class_="component recipe-ingredients-new container").findAll("span", class_="ingredients-item-name")
        directions_list = results_page.find("section", class_="recipe-instructions recipe-instructions-new component container").findAll("div", class_="section-body")
        name = results_page.find("h1", class_="headline heading-content").getText()
        for index in range(len(page_list)):
            ingredient = page_list[index].getText().strip()
            ingredient_list.append(ingredient)
        for index in range(len(directions_list)):
            direction = directions_list[index].getText().strip()
            directions.append(direction)
        dictionary['ingredients'] = ingredient_list
        dictionary['directions'] = directions
        dictionary['name'] = name
        dictionary['url'] = url
        return dictionary
    #except:
        #return ["No recipe found"]
def extractIngredientsType1(url):
    response = requests.get(url)
    results_page = BeautifulSoup(response.content, 'lxml')
    #try:
    if True:
        dictionary = {}
        ingredient_list = []
        directions = []
        ingredient_page_list = results_page.find("section", class_="ar_recipe_index full-page").findAll("span", itemprop="recipeIngredient")
        directions_list = results_page.findAll("span", class_="recipe-directions__list--item")
        name = results_page.find("h1", itemprop="name").getText()
        for index in range(len(ingredient_page_list)):
            ingredient = ingredient_page_list[index].getText()
            ingredient_list.append(ingredient)
        for index in range(len(directions_list)):
            direction = directions_list[index].getText().strip()
            directions.append(direction)
        dictionary['ingredients'] = ingredient_list
        dictionary['directions'] = directions
        dictionary['name'] = name
        dictionary['url'] = url
        return dictionary
    #except:
        #return ["No recipe found"]
def findIngredients(SEARCH_PHRASE):
    url = "https://www.allrecipes.com/search/results/?wt=" + SEARCH_PHRASE + "&sort=re"
    response = requests.get(url)
    #print(response.status_code)
    results_page = BeautifulSoup(response.content, 'lxml')
    try:
        recipeLink = results_page.find("article", class_="fixed-recipe-card").find("a", class_="fixed-recipe-card__title-link").get('href')
        return extractIngredientsType1(recipeLink)
    except:
        try:
            recipeLink = results_page.find("article", class_="fixed-recipe-card").find("a", class_="fixed-recipe-card__title-link").get('href')
            return extractIngredientsType2(recipeLink)
        except:
            return ["No recipe found"]
def ingredientsDirections(RECIPE_REQUEST):
    dictionary = findIngredients(RECIPE_REQUEST)
    reddit_link = '[' + dictionary['name'] + '](' + dictionary['url'] + ')'
    commentReply = reddit_link + ":  \n\n**The ingredients are:**" + "  \n\n" + "  \n".join(dictionary['ingredients']) + "  \n\n**The directions are:**\n\n•" + "  \n•".join(dictionary['directions'])
    commentReply = commentReply[:-2]
    return commentReply
def runBot(SUBREDDIT, KEYPHRASE):
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(SUBREDDIT)
    for comment in subreddit.stream.comments(skip_existing=True):
        print("************************")
        print(comment.body)
        if KEYPHRASE in comment.body.lower():
            winsound.Beep(2500, 1000)
            text = eraseUpTo(comment.body.lower(), KEYPHRASE)
            text = findSentence(text)
            if text.isspace() or text == "":
                comment.reply("Invalid entry")
            else:
                try:
                    reply = ingredientsDirections(text)
                    comment.reply(reply)
                    print("Replied: " + reply)
                    time.sleep(2)
                except:
                    reply = "Recipe not found"
                    comment.reply(reply)
                    print("Replied: " + reply)
                    time.sleep(2)
def main():
    SUBREDDIT = "testingground4bots"
    KEYPHRASE = "!recipe"
    runBot(SUBREDDIT, KEYPHRASE)
main()
#print(ingredientsDirections("flan"))

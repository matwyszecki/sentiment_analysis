import operator
from collections import Counter
import matplotlib.pyplot as plt
import re
from twitter_scraper import get_tweets


def readFile(path, split):
    text = open(path, 'r')
    if split == True:
        textWords = text.read().split()
    else:
        textWords = text.read()
    text.close()
    return textWords


def countWords(source, reference):
    wordsNum = 0
    source = map(str.lower, source)
    for word in source:
        if word in reference:
            wordsNum += 1
    return wordsNum


def remStopwords(source, reference):
    source = map(str.lower, source)
    pureText = []
    for word in source:
        if word not in reference:
            pureText.append(word)
    return pureText


def wordPercent(source, reference):
    words = countWords(source, reference)
    percent = (words/len(source))*100
    return round(percent, 1)


def mostCommon(source, reference):
    source = map(str.lower, source)
    mostCommonWords = []
    for word in source:
        if word in reference:
            mostCommonWords.append(word)

    mostCommonWords = Counter(mostCommonWords)  # Słownik

    dictList = []
    for key, value in mostCommonWords.items():  # Lista krotek
        dictList.append((key, value))

    dictList.sort(key=operator.itemgetter(1), reverse=True)

    shortDictList = []
    limit = 9
    for index, item in enumerate(dictList):
        shortDictList.append(item)
        if index == limit:
            break
    return shortDictList


def pieChart(values, labels, title):
    plt.pie(values, labels=labels,)
    plt.title(title)


def doublePieChart(values, labels, values2, labels2, title):
    fig, axs = plt.subplots(2)
    fig.suptitle(title)
    axs[0].pie(values, labels=labels,)
    axs[0].set_title('Tekst pierwszy')
    axs[1].pie(values2, labels=labels2,)
    axs[1].set_title('Tekst drugi')
    plt.show()


def mostCommonBar(source, reference):
    dict = mostCommon(source, reference)
    plt.bar(range(len(dict)), [val[1] for val in dict], align='center')
    plt.xticks(range(len(dict)), [val[0] for val in dict])
    plt.xticks(rotation=70)


def genAnalysis(source, negWords, posWords):
    negWordsCount = countWords(source, negWords)
    posWordsCount = countWords(source, posWords)
    if negWordsCount > posWordsCount:
        result = "Tekst jest nacechowany negatywnie"
    elif negWordsCount < posWordsCount:
        result = "Tekst jest nacechowany pozytywnie"
    elif negWordsCount == posWordsCount:
        result = "Tekst jest neutralny"
    return result


def percentAnalysis(source, negWords, posWords):
    pos = wordPercent(source, posWords)
    neg = wordPercent(source, negWords)
    neut = round(100 - wordPercent(source, posWords) -
                 wordPercent(source, negWords), 1)
    return pos, neg, neut


def results(pos, neg, neut):
    print("Słowa pozytywne: ", pos, "%", sep='')
    print("Słowa negatywne: ", neg, "%", sep='')
    print("Słowa neutralne: ", neut, "%", sep='')


def twitter(nick):
    twitter = open('twitter.txt', 'w', encoding="utf-8")
    tweetList = []
    for tweet in get_tweets(nick, pages=5):
        tweetList.append(tweet['text'])

    twitter.write(str(tweetList))
    twitter.close()


def main():
    posWords = readFile('positive-words.txt', True)
    negWords = readFile('negative-words.txt', True)
    stopWords = readFile('stopwords.txt', True)
    print("\nRodzaje analizy:")
    print("1: Analiza ogólna")
    print("2: Analiza procentowa")
    print("3: Najczęstsze pozytywne słowa")
    print("4: Najczęstsze negatywne słowa")
    print("5: Analiza dla słowa kluczowego")
    print("6: Analiza bez stopwords")
    print('7: Porównanie z innym tekstem')
    print('8: Analiza profilu na Twitterze')
    print("9: Zapisz wyniki analizy")
    print("10: Załaduj nowy plik")
    print("11: Zamknij program\n")
    path = input("Podaj scieżkę do pliku: ")
    while True:
        try:
            sourceFile = readFile(path, True)
        except FileNotFoundError:
            print("Nie ma takiego pliku.")
            main()
        finally:
            tryb = int(input("\nWybierz numer analizy: "))
            if tryb == 1:  # Analiza ogólna
                result = genAnalysis(sourceFile, negWords, posWords)
                print(result)
                negWordsCount = countWords(sourceFile, negWords)
                posWordsCount = countWords(sourceFile, posWords)
                print("Liczba słów pozytywnych: ", posWordsCount)
                print("Liczba słów negatywnych: ", negWordsCount)

            elif tryb == 2:  # Analiza procentowa
                pos, neg, neut = percentAnalysis(sourceFile, negWords, posWords)
                results(pos, neg, neut)
                pieChart([pos, neg, neut], ['Słowa pozytywne', 'Słowa negatywne',
                                            'Słowa neutralne'], "Rozkład procentowy słów nacechowanych emocjonalnie")
                plt.show()

            elif tryb == 3:  # Najczęstsze pozytywne słowa
                list = mostCommon(sourceFile, posWords)
                for item in list:
                    print(*item, sep=': ')
                mostCommonBar(sourceFile, posWords)
                plt.show()

            elif tryb == 4:  # Najczęstsze negatywne słowa
                list = mostCommon(sourceFile, negWords)
                for item in list:
                    print(*item, sep=': ')
                mostCommonBar(sourceFile, negWords)
                plt.show()

            elif tryb == 5:  # Analiza dla słowa kluczowego
                sourceFile = readFile(path, False)

                sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', sourceFile)
                key = input("Słowo kluczowe: ")

                keySent = []
                for sent in sentences:
                    if key in sent:
                        keySent.append(sent)

                keySent = " ".join(keySent)
                sourceFile = keySent.split()

                pos, neg, neut = percentAnalysis(sourceFile, negWords, posWords)
                result = genAnalysis(sourceFile, negWords, posWords)
                print(result)
                negWordsCount = countWords(sourceFile, negWords)
                posWordsCount = countWords(sourceFile, posWords)
                print("Liczba słów pozytywnych: ", posWordsCount)
                print("Liczba słów negatywnych: ", negWordsCount)
                results(pos, neg, neut)
                pieChart([pos, neg, neut], ['Słowa pozytywne', 'Słowa negatywne',
                                            'Słowa neutralne'], "Rozkład procentowy słów nacechowanych emocjonalnie")
                plt.show()

            elif tryb == 6:  # Analiza bez stopwords
                sourceFile = remStopwords(sourceFile, stopWords)

                pos, neg, neut = percentAnalysis(sourceFile, negWords, posWords)
                result = genAnalysis(sourceFile, negWords, posWords)
                print(result)
                negWordsCount = countWords(sourceFile, negWords)
                posWordsCount = countWords(sourceFile, posWords)
                print("Liczba słów pozytywnych: ", posWordsCount)
                print("Liczba słów negatywnych: ", negWordsCount)
                results(pos, neg, neut)
                pieChart([pos, neg, neut], ['Słowa pozytywne', 'Słowa negatywne',
                                            'Słowa neutralne'], "Rozkład procentowy słów nacechowanych emocjonalnie")
                plt.show()

            elif tryb == 7:  # Analiza porównawcza
                path2 = input("Ścieżka do drugiego pliku: ")
                try:
                    sourceFile2 = readFile(path2, True)
                except FileNotFoundError:
                    print("Nie ma takiego pliku.")
                    main()
                finally:
                    pos, neg, neut = percentAnalysis(sourceFile, negWords, posWords)
                    print("\nWyniki pierwszego tekstu:")
                    results(pos, neg, neut)

                    pos2, neg2, neut2 = percentAnalysis(sourceFile2, negWords, posWords)
                    print("Wyniki drugiego tekstu:")
                    results(pos2, neg2, neut2)
                    doublePieChart([pos, neg, neut], ['Słowa pozytywne', 'Słowa negatywne',
                                                      'Słowa neutralne'], [pos2, neg2, neut2], ['Słowa pozytywne', 'Słowa negatywne', 'Słowa neutralne'], 'Porównanie nacechowania dwóch tekstów:')
            elif tryb == 8:
                try:
                    nick = input("Podaj nazwę profilu na Twitterze: ")
                    twitter('{}'.format(nick))
                    sourceFile = readFile('twitter.txt', True)
                    result = genAnalysis(sourceFile, negWords, posWords)
                    print(result)
                    negWordsCount = countWords(sourceFile, negWords)
                    posWordsCount = countWords(sourceFile, posWords)
                    print("Liczba słów pozytywnych: ", posWordsCount)
                    print("Liczba słów negatywnych: ", negWordsCount)
                    pos, neg, neut = percentAnalysis(sourceFile, negWords, posWords)
                    results(pos, neg, neut)
                    pieChart([pos, neg, neut], ['Słowa pozytywne', 'Słowa negatywne',
                                                'Słowa neutralne'], "Rozkład procentowy słów nacechowanych emocjonalnie")
                except:
                    print("Nie ma takiego profilu")
                    main()
                plt.show()
            elif tryb == 9:
                wyniki = open('wyniki.txt', 'w')
                wyniki.write("Wyniki analizy tekstu: ")
                first = genAnalysis(sourceFile, negWords, posWords)
                wyniki.write(first)
                pos, neg, neut = percentAnalysis(sourceFile, negWords, posWords)
                wyniki.write("\nSłowa pozytywne: {} %".format(pos))
                wyniki.write("\nSłowa negatywne: {} %".format(neg))
                wyniki.write("\nSłowa neutralne: {} %".format(neut))
                wyniki.write("\nNajczęstsze pozytywne słowa:\n")
                list = mostCommon(sourceFile, posWords)
                for item in list:
                    wyniki.write(str(item))
                wyniki.write("\nNajczęstsze negatywne słowa:\n")
                list2 = mostCommon(sourceFile, negWords)
                for item in list2:
                    wyniki.write(str(item))
                wyniki.close()
                pieChart([pos, neg, neut], ['Słowa pozytywne', 'Słowa negatywne',
                                            'Słowa neutralne'], "Rozkład procentowy słów nacechowanych emocjonalnie")
                plt.savefig('wyniki_ogolne.png')
            elif tryb == 10:
                main()
            elif tryb == 11:
                break
            else:
                print("Błędne polecenie. Spróbuj jeszcze raz.\n")
                main()


main()

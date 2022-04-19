from queue import PriorityQueue  # importujemy PriorityQueue


# tworzymy klasę Node, która będzie podstaowym budulcem drzewa kodowania
# będzie ona przechowywać wartość, lewe i prawe dziecko, zakodowaną wartość, a także znak
class Node:
    value = 0
    right = None
    left = None
    character = ""

    def isLeaf(self):  # pomocnicza metoda, która pozwoli określić, czy liść przechowuje znak
        return self.character != ""

    def __init__(self, val, ch):  # definiujemy konstruktor
        self.value = val
        self.character = ch

    # funkcja __lt__ pomoże nam przy tworzeniu priority_queue
    def __lt__(self, other):
        if self.value != other.value:  # wykonujemy normalne porównanie, jeżeli liście są różne;
            return self.value < other.value
        if not self.isLeaf() and other.isLeaf():  # w przeciwnym wypadku ważniejsze są liście mające znak
            return True
        if self.isLeaf() and not other.isLeaf():  # w przeciwnym wypadku ważniejsze są liście mające znak
            return False
        if self.isLeaf() and other.isLeaf():  # jeżeli jednak oba maja znak, to decyduje kolejność alfabetyczna
            return ord(self.character[0]) < ord(other.character[0])
        return True


# Definiujemy metodę, która stworzy drzewo kodowania Huffmana, a następnie zwróci jego korzeń
# Argumentem jest tekst, który chcemy zakodować
def createTree(text):
    occurences = {}
    for c in text:  # zliczamy wystąpienia każdego znaku w tekście
        if occurences.__contains__(c):
            occurences[c] += 1
        else:
            occurences[c] = 1
    # Tworzymy obiekt PriorityQueue(), który będzie przechowywać nieprzypisane elementy drzewa.
    # Obiekt priority_queue pozwoli nam stworzyć uporządkowaną listę liści drzewa - najmniejsze będą najwyżej.
    nodes = PriorityQueue()
    for c in occurences.keys():  # tworzymy liście drzewa, bazując na znakach i ich ilości wystąpień, a następnei dodajmy do listy
        node = Node(occurences[c], c)
        nodes.put(node)
    rootNode = None  # tworzymy zmienna przechowujaca docelowo korzen drzewa
    while nodes.qsize() > 1:  # następnie iterujemy, dopóki w nodes nie zostanie ostatni element - korzeń drzewa
        n1 = nodes.get()  # pobieramy pierwszy, najmniejszy element z PriorityQueue
        n2 = nodes.get()  # pobieramy kolejny, najmniejszy element z PriorityQueue
        # jeżeli oba liście mają tą samą wartość, a jeden z nich jest kontenerem, to powinien on być traktowany jako większy element
        if n1.value == n2.value and not n1.isLeaf():
            pom = n1  # dlatego w takiej sytuacji podmieniamy wskaźniki
            n1 = n2
            n2 = pom
        parent = Node(n1.value + n2.value,
                      "")  # tworzymy liść-kontener, który będzie przechowywać dwa powyższe elementy i sumę ich wartości
        rootNode = parent  # ustawiamy go na aktualny korzen
        parent.left = n1  # i dodajemy mu dzieci
        parent.right = n2
        nodes.put(parent)  # a następnie dodajemy go do PriorityQueue
    return rootNode  # nasze drzewo jest gotowe - zwracamy korzeń


# tworzymy funkcję, która zakoduje drzewo
# jednocześnie zakoduje ona podany przez użytkownika tekst
def encodeValues(n, str, txt):
    if n is None:  # jeżeli trafimy na koniec drzewa
        return txt  # przerywamy rekurencję
    if n.isLeaf():  # jeżeli przechowuje on znak
        print(n.character + " : " + str)  # to drukujemy go wraz z zakodowaną wartością
        txt = txt.replace(n.character, str)  # a następnie podmieniamy znak w tekście z zakodowaną wartościa
    txt = encodeValues(n.left, str + "0", txt)  # wykonujemy te same działania dla lewej części drzewa - rekurencja
    txt = encodeValues(n.right, str + "1", txt)  # wykonujemy te same działania dla prawej części drzewa - rekurencja
    return txt  # na koniec zwracamy zakodowany tekst


# definiujemy funkcję, która odkoduje tekst na bazie utworzonego drzewa
def decode(root, text):
    decoded = ""  # zmienna pomocnicza
    currNode = root  # aktualnie rozważany element drzewa
    for char in text:  # iterujemy poprzez znaki zakodowanego tekstu
        if char == '0':  # jeżeli jest to 0, to oznacza, że musimy iśc na lewą stronę
            if currNode.left.isLeaf():  # jeżeli element po lewo jest liściem
                decoded += currNode.left.character  # to dodajemy jego znak do zmiennej pomocniczej
                currNode = root  # a następnie wracamy na początek drzewa
            else:
                currNode = currNode.left  # jeżeli trafiliśmy na kontener, to od niego zaczniemy nast. iterację
        else:  # jeżeli jest to 1, to oznacza, że musimy iśc na prawą stronę
            if currNode.right.isLeaf():  # jeżeli element po prawo jest liściem
                decoded += currNode.right.character  # to dodajemy jego znak do zmiennej pomocniczej
                currNode = root  # a następnie wracamy na początek drzewa
            else:
                currNode = currNode.right  # jeżeli trafiliśmy na kontener, to od niego zaczniemy nast. iterację
    return decoded  # zwracamy odkodowana wartosc


word = input("Kodowanie Huffmana. Podaj tekst, który chcesz zakodować:").rstrip()
rootNode = createTree(word)
print("Oto tablica kodowania:")
word = encodeValues(rootNode, "", word)
print("Oto tekst po zakodowaniu: " + word)
word = decode(rootNode, word)
print("Oto odkodowany tekst: " + word)
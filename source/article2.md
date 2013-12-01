## C 語言秘技 (1) – 使用 sscanf 模仿正規表達式的剖析功能 (作者：陳鍾誠)

在本系列文章中，我們將會陸續介紹一些 C 語言當中比較不常見，但是卻很強大的用法，希望透過這一系列的文章，能讓讀者感受到 C 語言的威力。

### 前言

從 1972 年 Dennis Ritchie 在貝爾實驗室發明 C 語言至今，已經過了將近四十個年頭。在這個變化快速的電腦世界裡，C 語言彷彿成了不變的避風港。四十年來，C 語言的改變並不多，而且一直都是所有作業系統底層的主力語言。近來，由於 Linux 與開放原始碼的發展，C 語言的影響力更為增強。在這裡，我不禁要問一個問題，為何 C 語言可以經過四十年而幾乎毫不改變。

C 語言很快，這或許是原因之ㄧ，但是像 Pascal 或 Fortran 等語言也幾乎與 C 語言一樣快，那又為何非 C 語言不可。但是，C 語言不只是快，還具有指標，容易與組合語言連結，具有巨集、條件式編譯、inline 函數、結構化、可以使用記憶體映射輸出入，因此可以用高階語言撰寫低階輸出入驅動程式，還有撰寫作業系統。

這些特性，讓 C 語言特別適合撰寫嵌入式系統，而嵌入式系統的環境，基本上也就是讓電腦退化到幾十年前的狀態，很小的記憶體、很慢的 CPU、通常沒有硬碟等等。今日的嵌入式系統，有點神似當年 Dennis Ritchie 所面對的環境，在很克難的資源中，發展出強大的作業系統。

UNIX 正是催生 C 語言的主要動力，當年 Ken Thompson 與 Dennis Ritchie 正是為了發展 UNIX 而設計出 C 語言的，這兩人也因為 UNIX/C 的貢獻而被 ACM 授予 Turing Award 這的電腦界的諾貝爾獎。

在 1978 年，Dennis 與另一位共同作者 Brian Wilson Kernighan 合力撰寫了第一本廣為流傳的 C 語言教科書，而這個版本的教科書由於影響深遠，成為人手一冊的 C 語言經典，因此後來我們這個版本的 C 語言教科書簡稱為 K&R 版本，
這個經典書籍中所使用的 C 語言版本也因此而被稱為 K&R 版的 C 語言，以便與後來 1988 年的 ANSI C 版本，以及 1999 年的 ISO C99 版本有所區隔。 (一個很容易誤會的點是， Ken Thompson 與 Brian Wilson Kernighan 是不同的兩個人，Ken Thompson 是發明 UNIX 與 C 語言的那個 Turing Award 得獎者，但是 Brian Wilson Kernighan 則是 C 語言書籍的作者，這兩個人的名字雖然都以 K 開頭，但是此 K 非比 K，請讀者切勿混淆)。

因此，學習 C 語言的人，如果只是將 C 當作是一般的程式語言，就會難以體會 C 語言的威力之所在，我們必須進入嵌入式與作業系統的領域，才能體會 C 語言的優點。一但您能夠體會這些優點，C 語言將不再僅僅是一個普通的語言，您也將能體會為何 C 語言會經歷四十年而不墬。然後，您也才能發揮 C 語言的能力，並且體會這些設計背後的優點與缺點。

### C 語言的優缺點

C 語言並非沒有缺點的，實際上，C 語言的缺點非常的多，多到可以用罄竹難書來形容。舉例而言，用 C 語言寫程式很容易有 bug，特別是在記憶體分配與回收這部份更是如此。C 語言沒有自動記憶体回收機制，沒有垃圾收集功能，因此常常導致忘記釋放記憶體，或者將同一個記憶體釋放數次，因而造成錯誤。C 語言的字串很原始，使用起來非常不方便。C 語言的標準函式庫甚至沒有基本的資料結構，像是陣列、串列、堆疊、字典等相關結構的函式庫。C 語言的條件式編譯讓程式看起來很冗長，使用標頭檔 *.h 讓你必需重複撰寫函數表頭，浪費許多時間。更糟的是，由於 C 語言的標準函式庫很小，因此在不同的平台上，每個廠商都實作出完全不同的函式庫，這導致 C 語言的程式難以跨越平台執行，您必須位每個平台打造一份程式，而不像 Java 那樣可以 Write Once，Run Anywhere。

但是，即便有了這麼多的缺點，C 語言仍然歷經四十年而不衰，這又是為甚麼呢？

每個 C 語言的缺點，幾乎都是伴隨著其優點而來的，C 語言的記憶體難以管理，是因為 C 語言具有強大的指標功能。字串函數很原始，是為了讓您可以使用字元陣列的方式處理字串，而不需要使用動態記憶體配置。無法跨越平台，是因為 C 語言適合用來打造底層的嵌入式系統，可以直接連結組合語言協同工作。從這個角度看來，C 語言的設計其實是相當精巧的，這也是 C 語言為何經歷四十年而不衰的原因。

### 學習 C 語言的好處

C 語言幾乎是當今被廣泛使用的語言當中，唯一同時具有高階與低階特性的語言，這個特性主要是由指標所造成的。利用指標，您可以用記憶體映射的方法存取記憶體，這讓 C 語言可以直接與周邊裝置溝通，因此許多裝置驅動程式可以用 C 語言撰寫，而不需要全部用組合語言。

學習 C 語言的投資報酬率，必須以數十年甚至一輩子的眼光來看，而不是短視的。程式語言多如過江之鯽，每隔兩三年就必須學習全新的語言，就像流行音樂或服飾一般，學會之後很快就會膩了。C 語言絕對不是流行的語言，而是一種經典的、長久的、耐用的語言，您在 C 語言的投資不會浪費，因為 C 語言將會陪伴您，走過數十年，甚至是一輩子。

### 密技 1 ：用 sscanf 剖析文字串

C 語言中的 scanf 函數，是初學者都會使用的，但也是大部分人都會誤用，或者是無法充分發揮其功能的。

C 語言的 sscanf() 與 ssprintf() 這兩個函數，採用的是一種既創新又好用的設計法，

事實上，函數 sscanf() 比 scanf() 更為好用，sscanf() 甚至支援了類似 Regular Expression 的功能，可以讓我們輕易的剖析格式化的字串。

sscanf 的函數原形如下，其中的 format 格式字串具有複雜的格式指定功能，以下我們將詳細說明這些格式的用途。

```CPP
int sscanf ( const char * str, const char * format, ...);

str : 被剖析的字串
format: 剖析格式

在 format 字串中，以 % 起頭者為剖析段落，通常在剖析完成後會指定給後面的變數，其格式語法如下：

剖析段落的語法：%[*][width][modifiers]type

  % 代表變數開始

  * 代表省略不放入變數中

  width 代表最大讀取寬度

  modifier 可以是 {h|I|L} 之一
  說明 : 其中 h 代表 2 byte 的變數 (像 short int)，
              l 代表 4 byte 的變數 (像 long int)，
              L 代表 8 byte 的變數 (像 long double)

  type 則可以是 c, d,e,E,f,g,G,o, s, u, x, X 等基本型態，
       也可以是類似 Regular Expression 的表達式。
  說明: c : 字元 (char); 
        d : 整數 (Decimal integer); 
        f : 浮點數 (Floating Point); 
        e,E : 科學記號 (Scientific notation); 
        g,G : 取浮點數或科學記號當中短的那個; 
    	o : 八進位 (Octal Integer); 
    	u : 無號數 (unsigned integer); 
    	x, X : 十六進位 (Hexadecimal integer)
```

為了說明 sscanf 函數的用法，我們寫了以下程式，以示範 format 欄位的各種寫法。

檔案：sscanf.c

```CPP
#include <stdio.h>

int main() {
  char name[20], tel[50], field[20], areaCode[20], code[20];
  int age;
  sscanf("name:john age:40 tel:082-313530", "%s", name);
  printf("%s\n", name);
  sscanf("name:john age:40 tel:082-313530", "%8s", name);
  printf("%s\n", name);
  sscanf("name:john age:40 tel:082-313530", "%[^:]", name);
  printf("%s\n", name);
  sscanf("name:john age:40 tel:082-313530", "%[^:]:%s", field, name);
  printf("%s %s\n", field, name);
  sscanf("name:john age:40 tel:082-313530", "name:%s age:%d tel:%s", name, &age, tel);
  printf("%s %d %s\n", name, age, tel);
  sscanf("name:john age:40 tel:082-313530", "%*[^:]:%s %*[^:]:%d %*[^:]:%s", name, &age, tel);
  printf("%s %d %s\n", name, age, tel);
  
  char protocol[10], site[50], path[50];
  sscanf("http://ccckmit.wikidot.com/cp/list/hello.txt", 
         "%[^:]:%*2[/]%[^/]/%[a-zA-Z0-9._/-]", 
    	 protocol, site, path);
  printf("protocol=%s site=%s path=%s\n", protocol, site, path);
  return 1;
}
```

其編譯執行結果如下所示。

```
D:\oc>gcc sscanf.c -o sscanf

D:\oc>sscanf
name:john
name:joh
name
name john
john 40 082-313530
john 40 082-313530
protocol=http site=ccckmit.wikidot.com path=cp/list/hello.txt
```

### 程式碼解析

您應該可以看到，在上述程式碼當中，所有的 %s, %d 等輸入欄位，預設都是以空白做為結尾的，例如以下指令就只會掃描到
`name="name:john"`，因為後面是空白了，所以就把 %s 的內容丟到了變數 name 當中。

```CPP
  sscanf("name:john age:40 tel:082-313530", "%s", name);
  printf("%s\n", name);
```

如果我們在 %s 等樣式中指定長度，像是以下這個 sscanf 所採用的 %8s，那麼掃描到 8 個字元之後就會停止了，所以此時 
`name="name:joh"` 。

```CPP
  sscanf("name:john age:40 tel:082-313530", "%8s", name);
  printf("%s\n", name);
```  

但是我們可以透過類似正規表達式的語法，來設定掃描的方式，舉例而言，像是以下的 sscanf 所採用的 `%[^:]` ，就讓我們
可以掃描到 `:` 符號為止，其中的樣式 `[^abc]` 符號代表不要比對 a, b, c 這些字元，所以 `[^:]` 代表的是不可比對到
 `:` 這個符號，因此就會在比對到該符號時停止了。於是掃描的結果會是 `name="name"` 。

```CPP
  sscanf("name:john age:40 tel:082-313530", "%[^:]", name);
  printf("%s\n", name);
```

當然、這些 %s, %d 等樣式之間還可以串接，以便進行連續掃描，因此下面這個 sscanf 指令可以一次掃出 field 與 name 兩個欄位，
結果會是 field="name", name="john" 。

```CPP
  sscanf("name:john age:40 tel:082-313530", "%[^:]:%s", field, name);
  printf("%s %s\n", field, name);
```

而且、在掃描到整數或浮點等非字串欄位時，還會將掃描到的結果轉為該型態放入變數中，例如下列 sscanf 指令中的 `&age` 欄位，
就會直接得到整數值，不需要像一般正規表達式那樣還需要經過轉型才能使用。

```CPP
  sscanf("name:john age:40 tel:082-313530", "name:%s age:%d tel:%s", name, &age, tel);
  printf("%s %d %s\n", name, age, tel);
```

如果我們希望某些欄位在掃描後，直接丟棄而不要存入任何變數中，那麼就可以用 `%*...` 這種加上 `*` 號的格式，此時 sscanf 會知道要將該欄位丟棄，不要存入到後面的變數裏。

```CPP
  sscanf("name:john age:40 tel:082-313530", "%*[^:]:%s %*[^:]:%d %*[^:]:%s", name, &age, tel);
  printf("%s %d %s\n", name, age, tel);
```

甚至、我們可以真的把 sscanf 當成「正規表達式」使用，只是語法稍有差異，功能也不像正規表達式那麼強，不過通常也夠用了。

舉例而言，以下的 sscanf 可以將一個網址剖析成 protocol, site, path 等三個段落，您可以看到我們使用的 `"%[^:]:%*2[/]%[^/]/%[a-zA-Z0-9._/-]"` 這個樣式，看起來是不是真的很像「正規表達式」呢？

```CPP
  char protocol[10], site[50], path[50];
  sscanf("http://ccckmit.wikidot.com/cp/list/hello.txt", 
         "%[^:]:%*2[/]%[^/]/%[a-zA-Z0-9._/-]", 
    	 protocol, site, path);
  printf("protocol=%s site=%s path=%s\n", protocol, site, path);
```

### 結語

對於很多想在 C 語言裏使用正規表達式的朋友來說，很可能沒有想過使用 sscanf 去取代 regex 之類的函式庫，但是經由以上的範例，您應該可以感覺到 sscanf 在某種程度上是可以替代「正規表達式」函式庫的，這樣我們就不需要引入 regex 之類的函式庫，除了節省程式碼所佔的空間之外，由於 sscanf 是標準函式庫，因此使用起來會更加容易。

況且、sscanf 可以直接將 %d %f 之類的參數放入整數與浮點數型態的變數當中，這樣還可以省下一道轉換的動作，因此、只要能夠用 sscanf 替代的功能，筆者通常不會引入正規表達式的函式庫，因為對筆者而言，在 C 當中使用 sscanf 比正規表達式更順手啊！

### 參考文獻
* <http://www.cplusplus.com/reference/clibrary/cstdio/sprintf/>
* <http://www.cplusplus.com/reference/clibrary/cstdio/sscanf/>


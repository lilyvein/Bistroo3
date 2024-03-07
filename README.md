# Sissejuhatus

Kooli bistrool on toidumenüü näitamiseks veebirakendus. Menüüd saab vaadata iga internetti
ühendatud arvutiga aadressil https://bistroo.kehtnakhk.ee/. Sama veebilehte näidatakse ka
bistroos seinal olevas televiisoris. Antud veebileht on loodud aastal 2018/2019 paiku. Seega on
see tänaseks natuke aegunud ning teil on vaja seda uuendada luues nii avalik vaade (front-end)
kui ka haldamise osa (back-end). Kogu projekt nii avalik vaade, kui haldamise osa on vaja teha
Django veebi projektina. Antud dokument räägib üldjoontes mida tuleb arendada. Sisaldab ka
inglisekeelset tõlget (ChatGPT).

# Projekti loomine

Projektil on kaks rakendust (applications). Haldamiseks on rakendus app_admin ja avalik
vaade on app_public. Mõlemad asuvad ühes projektis. Arendajal on ligipääs ka aadressile
/admin kuid sinna hilisem app_admin/ kasutaja ei pääse.

## Rakendus: app_admin

Esimene rakendus on app_admin, sest siin lehel toimub kõik see mida on võimalik avalikus
vaates (app_public) näha. Selleks, et antud rakendust luua tuleb vaadata avaliku menüüd. Kuna
see pole alati kõikide lisadega, siis vaata Ekraanitõmmis 1. Rakenduse ülesehitus peab olema
lihtne ja loogiline. Samas mingi asja tegemiseks ei tohiks üle paari kliki teha. Mõlemas
rakenduses kasutatakse ka Bootstrap stiile, et asi paistaks ilusam välja. App_admin puhul on
kujundus vaba, kuid ärge kirjuks asja ajage. Tekst peab olema lihtsalt loetav. Vajadusel võib
kasutada veel Font Awesome ikoonikesi. Kasutajaliides (UI) on kõikjal eestikeelne
kokkuleppel inglise keelne. Esimene asi mida tuleb hakata looma on kategooriad.
Kategooriad (Model Category)

Kategooriad on olulised, sest iga toidunimi käib kindlasse kategooriasse ja neid näidatakse
õiges kategooriate järjekorras vaata ekraanitõmmis 2. Kategooriad peavad olema just selles
järjekorras nagu ekraanitõmmisel on näha (Koolilõuna (v.a. sessioonõpe), Supid, Praed,
Lisandid, Kastmed, Salatid, Magustoidud). Kategooriate puhul peab arvestama, et neid võib
3
tulla juurde (näiteks Joogid), seega peab saama neid panna ka õigesse kohta. Avalikus vaates
peab olema Koolilõuna punane, kuid seda ei pea määrama kusagil mudeli (Model) loomisel.
Kategooriaid peab saama lisada, muuta, kustutada ja näidata. Sellepärast tuleb teha antud
mudelile CRUD (Create, Read, Update, Delete).

## Pealkirjad (Model Heading)

Pealkirjad on tekstid mida ei pruugi igal päeval olla. Vaata ekraanitõmmis 2. Pealkirjad on
kolm rida peale kuupäeva. Pealkirjade alla käib ka see sama kuupäev, sest kuidas muidu teada
millisel kuupäeval on millised pealkirjad. Seega pealkirjade puhul peab minimaalselt olema
kuupäev valitud, muud read on valikulised. Kuigi siin on üks oluline sõltuvus. Rohelist värvi
tekst pealkirjades on kaks rida. Need peavad olema mõlemad täidetud. Kui on Teema, siis on
ka Peakokk soovitab. Või kui on Peakokk soovitab, siis on ka Teema. Ainult ühte rida pole siin
lubatud täita. Toidud valmistasid võivad olla, kui ka puududa. Muidugi Teema ja Peakokk on
samuti valikulised, kuid eelpool mainitud tingimusega.

Nii nagu Kategooriate puhul nii ka Pealkirjade puhul tuleb teha CRUD. Kuni siiani on
mõlemad mudelid (Category, Heading) iseseisvad ja ei tea üksteisest midagi.

## Menüü (Model Menu and MenuItem) 

Mudel menüü (Menu) sisaldab kahte valikut. Kuupäeva pealkirjadest (Heading) ja kategooriat
(Category) kategooriatest. Peale selle valimist tuleks hakata täitama selle kategooria toite.
Vaikimisi (default) võiks näidata kolme tühja vormi, mis on seotud mudeli toidumenüü element
ehk toiduga (MenuItem). See mudel sisaldab toidunime, täishinda, pool hinda ja valikukasti
(Checkbox), kas näidata või mitte näidata menüüs. Vaata ekraanitõmmis 2. Selleks, et teada
mida avalikus vaates see valikukast teeb vaata ekraanitõmmis 3 (udustatud-/ähmastatud rida).
Toidunimi ja täishind peab olema täidetud. Täishinnaks on lubatud ka 0. Vaata
ekraanitõmmistelt kastmete hindu. Kui on tekst Prae hinna sees, siis on täishind ja pool hind
mõlemad 0. Tavaliselt on see ainult ühel kastmel, kuid pole teada, see võib ka mõne suvalise
muu toiduga nii olla.

Antud lahenduse puhul hakatakse näitama kuupäeva ja kategooriat, siis muutmine on lubatud
ainult jooksval päeval jooksvat menüüd (vanu menüüsid ei saa muuta). Hiljem saab vaadata
aga muuta mitte. Lubatud on kustutamine suvalisel ajal ja kustutatakse kogu kategooria. Seega
kui 29.10.2023 oli praadides kaks praadi, siis kustutatakse selle päeva prae kategooria koos
4
nende kahe praega. Üksikut elementi kategooriast kustutada ei saa (muutmisel tuleb teha
valikukasti Kustuta linnuke).

Nüüdseks on pealkirjad (Heading) seotud ka Menu ja MenuItem’iga, siis kui kustutatakse
kindla päeva pealkiri, siis kustuvad ka selle päeva kõik menüü kategooriad koos toitudega.
Ühel päeval on hetkel seitse kategooriat (koolilõunast magustoiduni).
Lisaks on nii ka kategooriatega. Kui kustutatakse kindla päeva kategooria, siis selle kategooria
toidud kaovad tehtud päeva menüüdest. Mõlemad on seotud mudeli tegemisel oleva
on_delete=models.CASCADE valikuga. Siin võib eksperimenteerida ka muude valikutega,
kuid siis tuleb ka mingi muu lahendus välja mõelda. Menüüd ei tohi veidralt õhku jääda kui
mingi seos on puudu/kustutatud.
# Mudelid loodud

Nüüd kui on mudelid loodud ja tundub, et asjad toimivad nagu vaja (CRUD), tuleb hakata
tegema avaliku vaadet (app_public).

## Rakendus: avalik vaade (app_public)

Avalikul vaatel kasutame 100% originaal kujundust. See on siis taustapilt, kirjastiil, teksti
värvid, läbivalt trükitähed (UPPERCASE). Taustapildi ja kirjastiili saab originaal veebilt
https://bistroo.kehtnakhk.ee/, neid linke siia ei ole pandud.
Menüü kaob ära iga päev peale südaööd. Seega kui menüüd pole siis tuleb ka teavitada, et
Menüüd pole veel sisestatud Vaata ekraanitõmmis 6. Loomulikult on ees ka uus kuupäev.
Mingit süsteemset veateadet ei tohiks siia tekkida kui menüüd pole.
Menüü näitamisel tuleb arvestada, et see on seinal ja seda lehte ei saa käsitsi uuendada nii nagu
oma veebilehitsejas teete (refresh). Seega tuleb välja mõelda lahendus, et ekraanil olev tekst ka
muutuks, kui midagi lisatakse või muudetakse.

## Täiendused

Kui avalik vaade on ka toimima saadud, siis on vaja teha veel rakendusse app_admin otsing.
Siin on mõeldud kindla kuupäeva menüüd ning otsing fraasi põhiselt.
5
## Otsing - kuupäev

Siin võiks olla olemasolevate kuupäevade nimekiri (Combobox) kust saab valida sobiva
kuupäeva ning näidatakse selle päeva menüü. Siin midagi erilist tekitama ei pea. Kogu menüü
kategooriate kaupa nii nagu avalik vaade aga disain on lihtsustatud. Siin ei pea olema disain
nagu avalikul vaatel. Selle päeva info peab lihtsalt näha olema. Sealhulgas pealkirjad, kui need
on olemas.
## Otsing - fraas

Siin on otsing sisestatud fraasi põhjal. Miinimum pikkus otsitaval fraasil on 3 või 4 tähte.
Pikkus sõltub lühema sõna järgi. Tulemuseks näidatakse kuupäev, kategooria, toidunimi ning
mõlemad hinnad. Otsing toimub toidu nimes. Tulemust näidatakse tabeli kujul. Ilmselt tuleb
siin kasutada ka leheküljendamist, sest aja jooksul asi kasvab. Uuemad on eespool ja vanemad
tagapool (kuupäeva järgi). Mitu kirjet leheküljendamisel näidatakse on teie valida. Antud info
võiks olla ka enne otsingut kasutajale teada.
# Muud

Nüüd võib lisada rakendusele app_admin ka kasutajapõhine logimine ja seadistada
administraatori osa kõik ainult sisselogimisega.

Päris admin leht (/admin) on arendajale ja sinna ei peaks peale arendaja keegi ligi pääsema.
Kasutajatel on kombeks aadressi real „mängida“, seega on vaja kirjutada ka vigade lehed (error
pages) 404 ja 500. Neid lehti on näha alles siis, kui seadetes (settings.py) on DEBUG=False
kirjutatud.
Lisaks on soovitav lugeda Difference Between Development, Stage, And Production
https://dev.to/flippedcoding/difference-between-development-stage-and-production-d0p Kõik
selleks, et millised peaks olema veebilehe seaded LIVE variandis (production). Siiani olete
toimetanud arendus variandis (development).
### Ekraanitõmmised

Dokumendi lõpus on veel terve rida ekraanitõmmiseid mida pole viidatud tekstis, kuid need on
teile juba alguses jagatud ekraanitõmmised. Need on projekti kaustas bistroo_menu_public_screenshots
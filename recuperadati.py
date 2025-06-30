import traceback
import time
import selenium
listacodici=[]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
opzioni=Options()
note_unisci=''
valori_uniti=''
conta_foto=int(0)
with open('listasku.csv','r') as file:
 for riga in file:
  listacodici.append(riga.strip())      
opzioni.add_argument('start-maximized')
browser=webdriver.Chrome(options=opzioni)
browser.get('https://www.bremboparts.com/europe/it')
elemento=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'Search')))
browser.find_elements(By.CLASS_NAME,'cookie-toast')[0].find_elements(By.CLASS_NAME,'close')[0].click()
time.sleep(1)
browser.find_elements(By.XPATH,"//button[text()='Confirm']")[0].click()
time.sleep(1)
browser.find_element(By.ID,'Search').find_elements(By.XPATH,".//div[@class='item'][.//button[@aria-label='Moto']]")[0].click()
pulsante_notifiche=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'notification-toast')))
browser.find_elements(By.CLASS_NAME,'notification-toast')[0].find_elements(By.XPATH,".//button[text()='Rifiuta']")[0].click()
time.sleep(1)
browser.find_element(By.ID,'Search').find_elements(By.XPATH,".//div[@class='item' and @data-type='type']")[0].find_elements(By.CLASS_NAME,'exp')[0].find_elements(By.CLASS_NAME,'item')[1].find_elements(By.CLASS_NAME,'button')[0].click()
time.sleep(1)
for codice in listacodici:
 try:
  conta_foto=0   
  risultato=''
  note_unisci=''
  valori_uniti=''
  descrizione=''
  browser.find_element(By.ID,'CodePrefix').clear()   
  browser.find_element(By.ID,'CodePrefix').send_keys(codice+Keys.ENTER)
  try:
   time.sleep(1)
   codice_errore=browser.find_elements(By.CLASS_NAME,'report-code')[0].find_elements(By.TAG_NAME,'span')[0].get_attribute('innerText').strip()
   if codice_errore:
    continue
  except Exception:
   pass     
  codice_trovato=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'main-title')))
  time.sleep(1)
  try: #BLOCCO DESCRIZIONE
   descrizione=browser.find_elements(By.CLASS_NAME,'description')[0].find_elements(By.CLASS_NAME,'content')[0].find_elements(By.XPATH,".//div[@class='mrg']")[0].get_attribute('innerText').replace('\n',' ').strip()   
  except Exception:
   traceback.print_exc()     
  try: #BLOCCO FOTO
   numero_foto=len(browser.find_element(By.ID,'Carousel').find_elements(By.TAG_NAME,'img'))
   for i in range(0,numero_foto):
    link_foto=browser.find_element(By.ID,'Carousel').find_elements(By.TAG_NAME,'img')[i].get_attribute('src')
    foto=link_foto+';'+str((i+1))
    conta_foto=conta_foto+1
    f=open('foto.csv','a')
    f.write('MQ-'+codice+';'+foto+"\n")
    f.close()
   link_singolo=browser.find_element(By.ID,('ProductDrawingZoomImage_'+codice)).find_elements(By.TAG_NAME,'img')[0].get_attribute('src')
   foto_singola=link_singolo+';'+str(conta_foto+1)
   f=open('foto.csv','a')
   f.write('MQ-'+codice+';'+foto_singola+"\n")
   f.close()
  except Exception:
   traceback.print_exc()   
  numero_note=len(browser.find_elements(By.CLASS_NAME,'description')[0].find_elements(By.CLASS_NAME,'content')[0].find_elements(By.XPATH,".//div[@data-type='detail' and @class='product-plus mrg']")[0].find_elements(By.CLASS_NAME,'item')) #BLOCCO NOTE
  try:
   for j in range(0,numero_note):
    nota_singola=browser.find_elements(By.CLASS_NAME,'description')[0].find_elements(By.CLASS_NAME,'content')[0].find_elements(By.XPATH,".//div[@data-type='detail' and @class='product-plus mrg']")[0].find_elements(By.CLASS_NAME,'item')[j].get_attribute('innerText')
    if note_unisci != '':
     note_unisci=note_unisci+'$'+nota_singola
    else:
     note_unisci=note_unisci+nota_singola+'$'   
   note_unisci.replace('$$','$')
  except Exception:
   traceback.print_exc()    
  try: #BLOCCO DATI TECNICI
   numero_dati=len(browser.find_elements(By.CLASS_NAME,'technical-data')[0].find_elements(By.CLASS_NAME,'content')[0].find_elements(By.CLASS_NAME,'data.mrg')[0].find_elements(By.CLASS_NAME,'item'))
   for k in range(0,numero_dati):
    nome_singolo=browser.find_elements(By.CLASS_NAME,'technical-data')[0].find_elements(By.CLASS_NAME,'content')[0].find_elements(By.CLASS_NAME,'data.mrg')[0].find_elements(By.CLASS_NAME,'item')[k].find_elements(By.CLASS_NAME,'label')[0].get_attribute('innerText').strip()
    valore_singolo=browser.find_elements(By.CLASS_NAME,'technical-data')[0].find_elements(By.CLASS_NAME,'content')[0].find_elements(By.CLASS_NAME,'data.mrg')[0].find_elements(By.CLASS_NAME,'item')[k].find_elements(By.CLASS_NAME,'detail')[0].get_attribute('innerText').strip()  
    dato_singolo=nome_singolo+': '+valore_singolo
    if valori_uniti != '':
     valori_uniti=valori_uniti+'$'+dato_singolo
    else:
     valori_uniti=valori_uniti+'$'+dato_singolo
   valori_uniti.replace('$$','$')
   print(valori_uniti)   
  except Exception:
   traceback.print_exc()
  f=open('dati.csv','a')
  f.write('MQ-'+codice+';'+note_unisci+';'+valori_uniti+';' + descrizione + "\n") 
  f.close()
  browser.find_elements(By.CLASS_NAME,'button.button-exp')[1].click()
  time.sleep(1)
  browser.find_elements(By.CLASS_NAME,'exp.show')[0].find_elements(By.CLASS_NAME,'item')[1].find_elements(By.TAG_NAME,'button')[0].click()
  time.sleep(2)  
 except Exception: #IN CASO DI ERRORE GENERICO TORNA ALLA PAGINA INIZIALE E INIZIA LA RICERCA DA LI
  traceback.print_exc()
  browser.get('https://www.bremboparts.com/europe/it')
  time.sleep(10)
  browser.find_element(By.ID,'Search').find_elements(By.XPATH,".//div[@class='item'][.//button[@aria-label='Moto']]")[0].click()
  time.sleep(1)
  browser.find_element(By.ID,'Search').find_elements(By.XPATH,".//div[@class='item' and @data-type='type']")[0].find_elements(By.CLASS_NAME,'exp')[0].find_elements(By.CLASS_NAME,'item')[1].find_elements(By.CLASS_NAME,'button')[0].click()
  time.sleep(1)
import csv
import os
import scrapy
import subprocess
import datetime



class GalpSolarSpider(scrapy.Spider):
    name = "galp_solar"

    def start_requests(self):
        #postal_codes = ['28001', '28002', '28003', '28004', '07800', '28005']  # list of Spanish postal codes
        postal_codes = ['00240', '00548', '01002', '01003', '01004', '01005', '01006', '01007', '01008', '01009', '01010', '01012', '01013', '01015',
                        '01110', '01117', '01118', '01120', '01128', '01129', '01130', '01138', '01139', '01160']
                        #'01165', '01169', '01170', '01171', '01191', '01192', '01193', '01194', '01195', '01196',
                        #'01200', '01206', '01207', '01208', '01211', '01212', '01213', '01216', '01220', '01230',
                        #'01250', '01260', '01300', '01306', '01307', '01308', '01309', '01320', '01321', '01322',
                        #'01330', '01340', '01400', '01408', '01409', '01420', '01423', '01426', '01427', '01428',
                        #'01430', '01439', '01440', '01449', '01450', '01468', '01470', '01474', '01476', '01477',
                        #'01478', '01479', '01510', '01520', '07800',  '02001', '02002', '02003', '02004', '02005',
                        #'02006', '02008', '02049', '02071', '02099', '02100', '02110', '02120', '02124', '02125',
                        #'02126', '02127', '02128', '02129', '02130', '02136', '02137', '02138', '02139', '02140',
                        #'02141', '02142', '02150', '02151', '02152', '02153', '02154', '02155', '02156', '02160',
                        #'02161', '02162', '02170', '02200', '02210', '02211', '02212', '02213', '02214', '02215',
                        #'02220', '02230', '02240', '02246', '02247', '02248', '02249', '02250', '02251', '02252',
                        #'02253', '02260', '02270', '02300', '02310', '02311', '02312', '02313', '02314', '02315',
                        #'02316', '02320', '02326', '02327', '02328', '02329', '02330', '02331', '02332', '02340',
                        #'02350', '02360', '02400', '02409', '02410', '02420', '02430', '02434', '02435', '02436',
                        #'02437', '02438', '02439', '02440', '02448', '02449', '02450', '02459', '02460', '02461',
                        #'02462', '02470', '02480', '02482', '02484', '02485', '02486', '02487', '02488', '02489',
                        #'02490', '02498', '02499', '02500', '02510', '02511', '02512', '02513', '02514', '02520',
                        #'02529', '02530', '02534', '02535', '02536', '02537', '02538', '02539', '02600', '02610',
                        #'02611', '02612', '02613', '02614', '02620', '02630', '02636', '02637', '02638', '02639',
                        #'02640', '02650', '02651', '02652', '02653', '02660', '02690', '02691', '02692', '02693',
                        #'02694', '02695', '02696', '02999', '03001', '03002', '03003', '03004', '03005', '03006',
                        #'03007', '03008', '03009', '03010', '03011', '03012', '03013', '03014', '03015', '03016',
                        # '03100', '03108', '03109', '03110', '03111', '03112', '03113', '03114', '03115', '03130',
                        #'03138', '03139', '03140', '03150', '03158', '03159', '03160', '03169', '03170', '28001',
                        #'28002', '28003', '28004' '28005', '07800']

        for postal_code in postal_codes:
            url = f"https://www.galpsolar.com/es/ayudas/buscador/?zipCode={postal_code}&channel=B2C"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        Municipio = response.xpath(
            '//*[@id="content"]/div/section[1]/div/div/div/div[1]/div/h1/b/text()').get()
        title_tiempo = response.xpath(
            '//*[@id="content"]/div/section[2]/div/div/div/div/div/div/div[1]/section/div/div/div/div[6]/div/div/div/p/text()').get()
        title_P = response.xpath(
            '//*[@id="content"]/div/section[2]/div/div/div/div/div/div/div[2]/section/div/div/div/div[8]/div/div/div/p[2]/text()').get()
        Cantidad_B = response.xpath(
            '//*[@id="content"]/div/section[2]/div/div/div/div/div/div/div[1]/section/div/div/div/div[9]/div/div/div/p[2]/text()').get()
        Duracion = response.xpath(
            '//*[@id="content"]/div/section[2]/div/div/div/div/div/div/div[2]/section/div/div/div/div[10]/div/div/div/p[2]/text()').get()

        yield {
            "postal_code": response.url.split("=")[-2].split("&")[0],
            "Municipio": Municipio,
            "title_tiempo": title_tiempo,
            "title_P": title_P,
            "Cantidad_B": Cantidad_B,
            "Duracion": Duracion,
            "title_scanned_at": str(datetime.datetime.now())
        }

           #spider
#def closed(self, reason):
#    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#    filename = f"IBI_{now}.csv"
#    with open(filename, 'w', newline='', encoding='utf-8') as f:
#        writer = csv.DictWriter(f, fieldnames=["postal_code", "Municipio", "title_tiempo", "title_P", "Cantidad_B",
#                                               "Duracion", "title_scanned"])
#        writer.writeheader()
#        for item in self.items:
#            item["title_scanned_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#            writer.writerow(item)

def closed(self, reason):
    filename = f"IBI_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["postal_code", "Municipio", "title_tiempo", "title_P", "Cantidad_B",
                                               "Duracion", "title_scanned"])
        writer.writeheader()
        for item in self.items:
            item["title_scanned_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(item)


if __name__ == '__main__':
    cmd = f"scrapy runspider GalpSolarSpider.py"
    os.system(cmd)

#subprocess.Popen(["open", 'GalpSolar.csv'], shell=True)

#'00240', '00548' ,'01001', '01002','01003' ,

# yelp spider
import scrapy
import re
import csv

# this spider will be used to crawl page results on yelp
class YelpSpider(scrapy.Spider):
    name = "yelp_spider"

    def start_requests(self):
        urls = [
            'https://www.yelp.com/search?find_desc=Restaurants&find_loc=60601&start=%d'
        ]
        self.csvFileHeaders()
        for url in urls:
            for i in range(0,1000, 10):
                yield scrapy.Request(url=url % i, callback=self.parse)

    def parse(self, response):
        address_selector = '.secondary-attributes address'
        SET_SELECTOR = '.indexed-biz-name'
        addresses = response.css(address_selector)
        businesses = response.css(SET_SELECTOR)

        # Remove the first element from the addresses array when no of addresses is more than no of businesses
        if len(addresses) > len(businesses):
            addresses.remove(addresses[0])

        for i in range(0, len(addresses)):
            if addresses[i] and len(addresses[i].xpath('text()'))>1:
                zip = addresses[i].xpath('text()')[1].extract().strip()[-5:]
                if zip != '60601':
                    continue
                else:
                    LINK_SELECTOR = 'a ::attr(href)'
                    link = businesses[i].css(LINK_SELECTOR).extract_first()
                    yield {
                        'link': link
                    }
                    if link is not None:
                        yield scrapy.Request(
                            response.urljoin(link),
                            callback=self.parseRestaurantContent
                        )


    def parseRestaurantContent(self, response):
        business_info_map = {}
        restaurant_map = {}

        NAME_SELECTOR = '.biz-page-title ::text'
        name = response.css(NAME_SELECTOR).extract_first()
        print(name.strip())
        business_info_map['name'] = name.strip()

        address1_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong/address/text()[1]'
        address2_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/strong/address/text()[2]'
        address1 = response.xpath(address1_selector).extract_first()
        if address1 is None: address1 = ""
        address2 = response.xpath(address2_selector).extract_first()
        if address2 is None: address2 = ""
        business_info_map['address'] = (address1 + ', ' + address2).strip()

        if '60601' not in business_info_map['address']:
            return

        location_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div/span[%d]/text()'
        location = ''
        for i in range(1,len(response.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]/div'))+1):
            location += response.xpath(location_selector % i)[0].extract().strip()

        business_info_map['location'] = business_info_map['address'] + " Neighborhood: " + location

        phone_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[4]/span[3]/text()'
        phone = response.xpath(phone_selector).extract_first()
        if phone is None: phone = ''
        business_info_map['phoneNumber'] = phone.strip()

        website_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[5]/span[2]/a/text()'
        website = response.xpath(website_selector).extract_first()
        if website is None: website = ""
        business_info_map['webSite'] = website.strip()

        review_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[1]/span/text()'
        review_count = response.xpath(review_selector).extract_first()
        if review_count is None: review_count = ''
        business_info_map['reviewCount'] = review_count.strip()

        for i in range(1,4):
            price_range_selector = '//*[@id="super-container"]/div/div/div[2]/div[1]/div/ul/li[%d]/div[2]/dl/dd/text()' % i
            price_range_name_selector = '//*[@id="super-container"]/div/div/div[2]/div[1]/div/ul/li[%d]/div[2]/dl/dt/text()' % i
            price_range = response.xpath(price_range_name_selector).extract_first()
            if price_range and price_range.strip() == "Price range":
                business_info_map['PriceRange'] = response.xpath(price_range_selector).extract_first().strip()

        categories_arr_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/span[2]/a'
        categories = response.xpath(categories_arr_selector)
        business_info_map['categories'] = ''
        for i in range(1, len(categories)+1):
            categories_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[3]/div[1]/div[2]/div[2]/span[2]/a[%d]/text()' % i
            category = response.xpath(categories_selector).extract_first()
            if i < len(categories):
                business_info_map['categories'] += category + ','
            else:
                business_info_map['categories'] += category

        rating_selector = '//*[@id="wrap"]/div[2]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/img/@alt'
        rating = response.xpath(rating_selector).extract()
        if not rating or len(rating) == 0: rating_number = ''
        else: rating_number = rating[0]
        business_info_map['rating'] = rating_number

        restaurant_id_selector = 'meta[name=yelp-biz-id] ::attr(content)'
        restaurant_id = response.css(restaurant_id_selector).extract_first()
        business_info_map['restaurantID'] = restaurant_id

        hours_selector = '.hours-table tbody tr'
        hours_arr = response.css(hours_selector)
        hours_data = ''
        for day_hours in hours_arr:
            day = (day_hours).xpath('th/text()').extract_first()
            hours = " ".join((day_hours).xpath('td')[0].xpath('span/text()').extract())
            hours_data += day + " " + hours + "\n"

        business_info_map['Hours'] = hours_data

        for k in range(1,4):
            right_pane_selector = '//*[@id="super-container"]/div/div/div[2]/div[2]/div[%i]/h3/text()' % k
            right_pane_content = response.xpath(right_pane_selector).extract_first()

            if right_pane_content and right_pane_content.strip() == "More business info":

                for j in range(1, 22):
                    business_info_name_selector = '//*[@id="super-container"]/div/div/div[2]/div[2]/div[%i]/ul/li/div/dl[%d]/dt/text()' % (k, j)
                    business_info_selector = '//*[@id="super-container"]/div/div/div[2]/div[2]/div[%i]/ul/li/div/dl[%d]/dd/text()' % (k, j)

                    business_name = response.xpath(business_info_name_selector).extract_first()
                    business_info = response.xpath(business_info_selector).extract_first()

                    if business_info and business_name:
                        print(business_name.strip(), business_info.strip())
                        business_info_map[business_name.strip().replace(" ", "").replace("-","")] = business_info.strip()
                    else:
                        print()

        print(business_info_map)
        self.restaurantOutput(business_info_map)


        request_url = response.request.url
        #if request_url

        review_page_number = response.css('.page-of-pages')[0].xpath('text()').extract_first().strip().split(" ")[1]
        if review_page_number:
            start = '&start='+str((int(review_page_number)) * 20)
            yield scrapy.Request(response.urljoin(request_url+start), callback=self.parseReview)
            #yield scrapy.Request(response.urljoin(request_url + start), callback=self.parseAuthor)

        #self.parseReview(response)
        #self.parseAuthor(response)

        restaurant_map[restaurant_id] = business_info_map

    def parseReview(self, response):
        review_map = {}
        # This section extracts the reviews
        reviews_selector = '.review-list'
        review_array = response.css(reviews_selector)[0].xpath('ul/li')

        for i in range(2,len(review_array)):
            review_id= review_array[i].xpath('div/@data-review-id').extract_first()
            review_map['reviewID'] = review_id.strip()

            restaurant_id_selector = 'meta[name=yelp-biz-id] ::attr(content)'
            restaurant_id = response.css(restaurant_id_selector).extract_first()
            review_map['businessID'] = restaurant_id

            user_id = review_array[i].xpath('div/@data-signup-object').extract_first()
            review_map['reviewerID'] = user_id[8:].strip()

            date = review_array[i].xpath('div/div[2]/div[1]/div/span/text()').extract_first()
            review_map['date'] = date.strip()

            content = review_array[i].xpath('div/div[2]/div[1]/p/text()').extract_first()
            if content is None: content = ''
            review_map['reviewContent'] = content.strip()

            rating = review_array[i].xpath('div/div[2]/div[1]/div/div/div/@title').extract_first()
            review_map['rating'] = rating.strip()

            useful_count = review_array[i].xpath('div/div[2]/div[2]/div/ul/li[1]/a/span[3]').extract_first()
            ucount = re.findall(r'>(.+?)<', useful_count.strip())
            if len(ucount) > 0: review_map['usefulCount'] = ucount[0]
            else: review_map['usefulCount'] = 0

            cool_count = review_array[i].xpath('div/div[2]/div[2]/div/ul/li[3]/a/span[3]').extract_first()
            ccount = re.findall(r'>(.+?)<', cool_count.strip())
            if len(ccount) > 0: review_map['coolCount'] = ccount[0]
            else: review_map['coolCount'] = 0

            funny_count = review_array[i].xpath('div/div[2]/div[2]/div/ul/li[2]/a/span[3]').extract_first()
            fcount = re.findall(r'>(.+?)<', funny_count.strip())
            if len(fcount) > 0: review_map['funnyCount'] = fcount[0]
            else: review_map['funnyCount'] = 0


        print(review_map)
        print(len(review_map))
        self.reviewOutput(review_map)
        self.parseAuthor(response)

    def parseAuthor(self, response):
        author_map = {}
        reviews_selector = '.review-list'
        review_array = response.css(reviews_selector)[0].xpath('ul/li')
        # author.csv ================

        for i in range(2, len(review_array)):
            user_id = review_array[i].xpath('div/@data-signup-object').extract_first()
            author_map['authorID'] = user_id[8:].strip()

            user_name = review_array[i].xpath('div/div[1]/div/div/div[2]/ul[1]/li[1]/a/text()').extract_first()
            author_map['name'] = user_name

            location = review_array[i].xpath('div/div[1]/div/div/div[2]/ul[1]/li[2]/b/text()').extract_first()
            author_map['location'] = location

            review_count = review_array[i].xpath('div/div[1]/div/div/div[2]/ul[2]/li[2]/b/text()').extract_first()
            author_map['reviewCount'] = review_count

            friend_count = review_array[i].xpath('div/div[1]/div/div/div[2]/ul[2]/li[1]/b/text()').extract_first()
            author_map['friendCount'] = friend_count

            photo_count = review_array[i].xpath('div/div[1]/div/div/div[2]/ul[2]/li[3]/b/text()').extract_first()
            author_map['photoCount'] = photo_count

        print(author_map)
        print(len(author_map))
        self.authorOutput(author_map)
        print("======================================================")



    def csvFileHeaders(self):
        with open('author.csv', 'w', newline='') as authorCSV:
            writer = csv.writer(authorCSV)
            writer.writerow(["authorID", "name", "location", "reviewCount", "friendCount", "photoCount"])

        with open('review.csv', 'w', newline='') as reviewCSV:
            writer = csv.writer(reviewCSV)
            writer.writerow(
                ["reviewID", "businessID", "reviewerID", "date", "reviewContent", "rating", "usefulCount", "coolCount",
                 "funnyCount"])

        with open('restaurant.csv', 'w', newline='') as restaurantCSV:
            writer = csv.writer(restaurantCSV)
            writer.writerow(
                ["restaurantID", "name", "location", "reviewCount", "rating", "categories", "address", "Hours",
                 "GoodforKids", "AcceptsCreditCards", "Parking", "Attire", "GoodforGroups", "PriceRange",
                 "TakesReservations", "Delivery", "Takeout", "WaiterService", "OutdoorSeating", "WiFi",
                 "GoodFor", "Alcohol", "NoiseLevel", "Ambience", "HasTV", "Caters", "WheelchairAccessible",
                 "webSite", "phoneNumber"])

    def authorOutput(self,authorDetails):
        if not authorDetails:
            return
        author_details = ["authorID", "name", "location", "reviewCount", "friendCount", "photoCount"]
        with open('author.csv', 'a', newline='') as authorCSV:
            writer = csv.writer(authorCSV)
            row = []
            for detail in author_details:
                if authorDetails.get(detail) is None: row.append('NULL')
                else: row.append(authorDetails.get(detail))

            writer.writerow(row)


    def reviewOutput(self, reviewDetails):
        if not reviewDetails:
            return
        review_details = ["reviewID", "businessID", "reviewerID", "date", "reviewContent", "rating", "usefulCount", "coolCount",
             "funnyCount"]

        with open('review.csv', 'a', newline='') as reviewCSV:
            writer = csv.writer(reviewCSV)
            row = []
            for detail in review_details:
                if reviewDetails.get(detail) is None: row.append('NULL')
                else: row.append(reviewDetails.get(detail))
            writer.writerow(row)


    def restaurantOutput(self,restaurantDetails):
        if not restaurantDetails:
            return

        restaurant_details = ["restaurantID", "name", "location", "reviewCount", "rating", "categories", "address",
                              "Hours",
                              "GoodforKids", "AcceptsCreditCards", "Parking", "Attire", "GoodforGroups", "PriceRange",
                              "TakesReservations", "Delivery", "Takeout", "WaiterService", "OutdoorSeating", "WiFi",
                              "GoodFor", "Alcohol", "NoiseLevel", "Ambience", "HasTV", "Caters", "WheelchairAccessible",
                              "webSite", "phoneNumber"]
        with open('restaurant.csv', 'a', newline='') as restaurantCSV:
            writer = csv.writer(restaurantCSV)
            row = []
            for detail in restaurant_details:
                if restaurantDetails.get(detail) is None or restaurantDetails.get(detail).strip() == '': row.append('NULL')
                else: row.append(restaurantDetails.get(detail))
            writer.writerow(row)

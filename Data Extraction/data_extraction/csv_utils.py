import csv


def csvFileHeaders():
    with open('author.csv', 'w') as authorCSV:
        writer = csv.writer(authorCSV)
        writer.writerow(["authorID", "name", "location", "reviewCount", "friendCount", "photoCount"])
        authorCSV.flush()
    authorCSV.close()

    with open('review.csv', 'w') as reviewCSV:
        writer = csv.writer(reviewCSV)
        writer.writerow(
            ["reviewID", "businessID", "reviewerID", "date", "reviewContent", "rating", "usefulCount", "coolCount",
             "funnyCount"])
        reviewCSV.flush()
    reviewCSV.close()

    with open('restaurant.csv', 'w') as restaurantCSV:
        writer = csv.writer(restaurantCSV)
        writer.writerow(["restaurantID", "name", "location", "reviewCount", "rating", "categories", "address", "Hours",
                         "GoodforKids", "AcceptsCreditCards", "Parking", "Attire", "GoodforGroups", "PriceRange",
                         "TakesReservations", "Delivery", "Takeout", "WaiterService", "OutdoorSeating", "WiFi",
                         "GoodFor", "Alcohol", "NoiseLevel", "Ambience", "HasTV", "Caters", "WheelchairAccessible",
                         "webSite", "phoneNumber"])
        restaurantCSV.flush()
    restaurantCSV.close()


def authorOutput(authorDetails):
    with open('author.csv', 'a') as authorCSV:
        writer = csv.writer(authorCSV)
        writer.writerow(authorDetails.values())
        authorCSV.flush()


def reviewOutput(reviewDetails):
    with open('review.csv', 'a') as reviewCSV:
        writer = csv.writer(reviewCSV)
        writer.writerow(reviewDetails.values())


def restaurantOutput(restaurantDetails):
    restaurant_details = ["restaurantID", "name", "location", "reviewCount", "rating", "categories", "address", "Hours",
                         "GoodforKids", "AcceptsCreditCards", "Parking", "Attire", "GoodforGroups", "PriceRange",
                         "TakesReservations", "Delivery", "Takeout", "WaiterService", "OutdoorSeating", "WiFi",
                         "GoodFor", "Alcohol", "NoiseLevel", "Ambience", "HasTV", "Caters", "WheelchairAccessible",
                         "webSite", "phoneNumber"]
    with open('restaurant.csv', 'a') as restaurantCSV:
        writer = csv.writer(restaurantCSV)
        row = []
        for detail in restaurant_details:
            row.append(restaurantDetails.get(detail))
        writer.writerow(row)


def main():
    author = {"authorID": 1, "name": "Alex", "location": "ABC", "reviewCount": 1, "friendCount": 1, "photoCount": 1}
    csvFileHeaders()
    authorOutput(author)


if __name__ == '__main__': main()




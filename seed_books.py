# seed_books.py
from libraryapp.models import Book

book_data = [
    ("Moby Dick", "Herman Melville", "Fiction",
     "A thrilling sea adventure following Captain Ahab's obsessive quest to kill the white whale. This edition features vintage nautical illustrations. Condition: Good — minor wear on cover.",
     5, "book1.jpg"),

    ("Pride and Prejudice", "Jane Austen", "Romance",
     "Elizabeth Bennet navigates love and societal expectations in 19th-century England, clashing with the proud but honorable Mr. Darcy. Condition: Excellent — clean pages and no markings.",
     4, "book2.jpg"),

    ("1984", "George Orwell", "Science Fiction",
     "A dystopian novel where Winston Smith battles a totalitarian regime and its omnipresent surveillance. A chilling classic about truth and freedom. Condition: Fair — some underlining and folded pages.",
     5, "book3.jpg"),

    ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction",
     "A story of wealth, love, and tragedy set in the roaring 1920s. Jay Gatsby’s longing for Daisy Buchanan leads to a grand illusion and heartbreaking end. Condition: Good — a few creased corners.",
     4, "book4.jpg"),

    ("To Kill a Mockingbird", "Harper Lee", "Drama",
     "In the Deep South, young Scout Finch observes injustice and courage as her father defends a Black man falsely accused of a crime. A powerful coming-of-age story. Condition: Excellent.",
     5, "book5.jpg"),

    ("Frankenstein", "Mary Shelley", "Horror",
     "Victor Frankenstein’s creation of a living being leads to horror, regret, and philosophical questions about responsibility. A gothic masterpiece. Condition: Good — some age-yellowing of pages.",
     4, "book6.jpg"),

    ("Brave New World", "Aldous Huxley", "Science Fiction",
     "A vision of a technologically engineered society where individuality is sacrificed for stability. Thought-provoking and eerily prescient. Condition: Very Good — light cover wear only.",
     4, "book7.jpg"),

    ("The Catcher in the Rye", "J. D. Salinger", "Coming-of-age",
     "Holden Caulfield’s sarcastic, sensitive journey through New York after being expelled. A raw, honest portrayal of teenage alienation. Condition: Good — some notes in margins.",
     5, "book8.jpg"),
]

for title, author, genre, description, rating, image in book_data:
    Book.objects.create(
        title=title,
        author=author,
        genre=genre,
        description=description,
        rating=rating,
        image=image,
        created_by="admin"
    )

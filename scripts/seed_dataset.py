"""
BookWise AI — Dataset Seeder & Synthesizer
Generates an authentic, curated dataset of classic and modern literature,
tech/AI, science, fiction, and philosophy with authentic ISBNs, authors,
descriptions, genres, publication dates, and OpenLibrary cover references.
Also generates a realistic user-item rating matrix for collaborative filtering.
"""
import os
import csv
import random

DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "datasets"))
os.makedirs(DATASET_DIR, exist_ok=True)

BOOKS_DATA = [
    # Science Fiction & Dystopian
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Science Fiction",
        "publication_year": 1965,
        "publisher": "Chilton Books",
        "isbn": "9780441172719",
        "average_rating": 4.26,
        "rating_count": 1245000,
        "description": "Set on the desert planet Arrakis, Dune tells the story of Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only valuable commodity is the spice melange, which extends life and enhances mental abilities.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780441172719-L.jpg"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genre": "Dystopian Fiction",
        "publication_year": 1949,
        "publisher": "Secker & Warburg",
        "isbn": "9780451524935",
        "average_rating": 4.19,
        "rating_count": 4320000,
        "description": "Winston Smith wrestles with oppression in Oceania, a totalitarian state ruled by the omnipresent Big Brother and the Party. A haunting warning against totalitarianism, surveillance, and truth manipulation.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg"
    },
    {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "genre": "Dystopian Fiction",
        "publication_year": 1932,
        "publisher": "Chatto & Windus",
        "isbn": "9780060850524",
        "average_rating": 3.99,
        "rating_count": 1820000,
        "description": "A dark utopian vision of a technologically conditioned society where happiness is manufactured, family structures are abolished, and individuality is traded for consumer stability and soma drugs.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780060850524-L.jpg"
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "genre": "Science Fiction",
        "publication_year": 1984,
        "publisher": "Ace",
        "isbn": "9780441569595",
        "average_rating": 3.90,
        "rating_count": 340000,
        "description": "The seminal cyberpunk novel following Case, a washed-up computer hacker hired by a mysterious employer to pull off the ultimate digital heist in the matrix of cyberspace against a sentient artificial intelligence.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780441569595-L.jpg"
    },
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "genre": "Science Fiction",
        "publication_year": 1951,
        "publisher": "Gnome Press",
        "isbn": "9780553293357",
        "average_rating": 4.17,
        "rating_count": 520000,
        "description": "Hari Seldon discovers the mathematical science of psychohistory, predicting the inevitable fall of the Galactic Empire and setting out to preserve humanity's knowledge across a thirty-thousand-year dark age.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553293357-L.jpg"
    },
    {
        "title": "Fahrenheit 451",
        "author": "Ray Bradbury",
        "genre": "Dystopian Fiction",
        "publication_year": 1953,
        "publisher": "Ballantine Books",
        "isbn": "9781451673319",
        "average_rating": 3.98,
        "rating_count": 2150000,
        "description": "Guy Montag is a fireman whose job is to burn forbidden books. When he meets a young neighbour who introduces him to the richness of literature and critical thought, Montag questions everything about his sterile society.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781451673319-L.jpg"
    },
    {
        "title": "Do Androids Dream of Electric Sheep?",
        "author": "Philip K. Dick",
        "genre": "Science Fiction",
        "publication_year": 1968,
        "publisher": "Doubleday",
        "isbn": "9780345404473",
        "average_rating": 4.09,
        "rating_count": 480000,
        "description": "In post-apocalyptic San Francisco, bounty hunter Rick Deckard is tasked with 'retiring' six rogue Nexus-6 androids posing as human beings, forcing him to question what truly defines humanity and empathy.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780345404473-L.jpg"
    },
    {
        "title": "The Left Hand of Darkness",
        "author": "Ursula K. Le Guin",
        "genre": "Science Fiction",
        "publication_year": 1969,
        "publisher": "Ace Books",
        "isbn": "9780441478125",
        "average_rating": 4.08,
        "rating_count": 220000,
        "description": "Human envoy Genly Ai journeys to the icy planet Gethen to convince its leaders to join the galactic federation, struggling to understand an ambisexual society devoid of gender dualities and war.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780441478125-L.jpg"
    },
    {
        "title": "Snow Crash",
        "author": "Neal Stephenson",
        "genre": "Science Fiction",
        "publication_year": 1992,
        "publisher": "Bantam Spectra",
        "isbn": "9780553380958",
        "average_rating": 4.03,
        "rating_count": 310000,
        "description": "Hiro Protagonist, a pizza delivery driver in reality and warrior prince in the Metaverse, uncovers an ancient Sumerian neurolinguistic virus threatening to crash both virtual networks and human brains.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553380958-L.jpg"
    },
    {
        "title": "The Three-Body Problem",
        "author": "Cixin Liu",
        "genre": "Science Fiction",
        "publication_year": 2008,
        "publisher": "Tor Books",
        "isbn": "9780765382030",
        "average_rating": 4.07,
        "rating_count": 395000,
        "description": "During China's Cultural Revolution, a secret military project sends signals into space, establishing contact with a dying alien civilization orbiting three chaotic suns, triggering Earth's greatest crisis.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765382030-L.jpg"
    },

    # AI, Computer Science & Tech Non-Fiction
    {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell & Peter Norvig",
        "genre": "Computer Science & AI",
        "publication_year": 2020,
        "publisher": "Pearson",
        "isbn": "9780134610993",
        "average_rating": 4.35,
        "rating_count": 18500,
        "description": "The definitive textbook on artificial intelligence, covering rational intelligent agents, search algorithms, probabilistic reasoning, machine learning, deep learning, NLP, computer vision, and robotics.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780134610993-L.jpg"
    },
    {
        "title": "Deep Learning",
        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "genre": "Computer Science & AI",
        "publication_year": 2016,
        "publisher": "MIT Press",
        "isbn": "9780262035613",
        "average_rating": 4.41,
        "rating_count": 14200,
        "description": "Written by three pioneers in machine learning, this text provides comprehensive theoretical mathematical foundations and practical algorithms for neural networks, backpropagation, CNNs, RNNs, and GANs.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780262035613-L.jpg"
    },
    {
        "title": "Superintelligence: Paths, Dangers, Strategies",
        "author": "Nick Bostrom",
        "genre": "Computer Science & AI",
        "publication_year": 2014,
        "publisher": "Oxford University Press",
        "isbn": "9780199678112",
        "average_rating": 3.87,
        "rating_count": 48000,
        "description": "An influential analysis exploring the profound implications of creating artificial general intelligence that surpasses human cognition, detailing existential safety risks and AI alignment strategies.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780199678112-L.jpg"
    },
    {
        "title": "Life 3.0: Being Human in the Age of Artificial Intelligence",
        "author": "Max Tegmark",
        "genre": "Computer Science & AI",
        "publication_year": 2017,
        "publisher": "Knopf",
        "isbn": "9781101946596",
        "average_rating": 4.02,
        "rating_count": 42000,
        "description": "MIT physicist Max Tegmark explores the upcoming technological revolution of conscious synthetic intelligence, examining ethical, socioeconomic, and cosmological consequences for the future of civilization.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781101946596-L.jpg"
    },
    {
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "genre": "Computer Science & AI",
        "publication_year": 2008,
        "publisher": "Prentice Hall",
        "isbn": "9780132350884",
        "average_rating": 4.40,
        "rating_count": 125000,
        "description": "Even bad code can function, but it brings development teams to their knees. Uncle Bob outlines principles, patterns, and refactoring practices for writing readable, maintainable, high-quality software.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg"
    },
    {
        "title": "The Master Algorithm",
        "author": "Pedro Domingos",
        "genre": "Computer Science & AI",
        "publication_year": 2015,
        "publisher": "Basic Books",
        "isbn": "9780465065707",
        "average_rating": 3.86,
        "rating_count": 19500,
        "description": "A tour through the five rival tribes of machine learning: Symbolists, Connectionists, Evolutionaries, Bayesians, and Analogizers, searching for the unified algorithm that can learn all knowledge from data.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780465065707-L.jpg"
    },
    {
        "title": "Algorithms to Live By: The Computer Science of Human Decisions",
        "author": "Brian Christian & Tom Griffiths",
        "genre": "Computer Science & AI",
        "publication_year": 2016,
        "publisher": "Henry Holt and Co.",
        "isbn": "9781627790369",
        "average_rating": 4.14,
        "rating_count": 92000,
        "description": "Fascinating exploration of how computer algorithms like optimal stopping, caching, sorting, and game theory can help humans solve everyday human problems like time management, finding an apartment, and making decisions.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781627790369-L.jpg"
    },
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "genre": "Computer Science & AI",
        "publication_year": 2017,
        "publisher": "O'Reilly Media",
        "isbn": "9781449373320",
        "average_rating": 4.72,
        "rating_count": 31000,
        "description": "The golden standard guide to distributed systems, relational versus NoSQL data models, consensus algorithms, replication, partitioning, stream processing, and building scalable fault-tolerant architectures.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781449373320-L.jpg"
    },

    # Fantasy & High Fantasy
    {
        "title": "The Fellowship of the Ring",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "publication_year": 1954,
        "publisher": "George Allen & Unwin",
        "isbn": "9780547928210",
        "average_rating": 4.38,
        "rating_count": 2750000,
        "description": "Young hobbit Frodo Baggins is entrusted with the One Ring of the Dark Lord Sauron. Accompanied by a brave fellowship of men, elves, dwarves, and wizards, he embarks on an epic quest to Mount Doom.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547928210-L.jpg"
    },
    {
        "title": "A Game of Thrones",
        "author": "George R.R. Martin",
        "genre": "Fantasy",
        "publication_year": 1996,
        "publisher": "Bantam Spectra",
        "isbn": "9780553103540",
        "average_rating": 4.44,
        "rating_count": 2420000,
        "description": "Noble houses vie for control of the Iron Throne of the Seven Kingdoms of Westeros while an ancient mythical enemy awakens in the far icy north beyond the Wall.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553103540-L.jpg"
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "genre": "Fantasy",
        "publication_year": 2007,
        "publisher": "DAW Books",
        "isbn": "9780756404741",
        "average_rating": 4.51,
        "rating_count": 870000,
        "description": "Kvothe, a legendary wizard and musician in hiding as an innkeeper, recounts his humble beginnings in an itinerant troupe, his tragic loss, and his daring education at the University of magic.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780756404741-L.jpg"
    },
    {
        "title": "The Way of Kings",
        "author": "Brandon Sanderson",
        "genre": "Fantasy",
        "publication_year": 2010,
        "publisher": "Tor Books",
        "isbn": "9780765326355",
        "average_rating": 4.65,
        "rating_count": 460000,
        "description": "Roshar is a harsh tempest-swept world where magical Shardblades change wars. A slave bridgeman named Kaladin discovers forgotten surge-binding powers during an endless campaign on the Shattered Plains.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765326355-L.jpg"
    },
    {
        "title": "Mistborn: The Final Empire",
        "author": "Brandon Sanderson",
        "genre": "Fantasy",
        "publication_year": 2006,
        "publisher": "Tor Books",
        "isbn": "9780765311788",
        "average_rating": 4.48,
        "rating_count": 630000,
        "description": "In an ash-choked empire ruled by an immortal tyrant, a street urchin named Vin discovers her rare Allomantic abilities to burn metals and joins a crew of thieves aiming to overthrow a god.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765311788-L.jpg"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "publication_year": 1937,
        "publisher": "George Allen & Unwin",
        "isbn": "9780547928227",
        "average_rating": 4.29,
        "rating_count": 3400000,
        "description": "Bilbo Baggins, a comfortable home-loving hobbit, is swept into a daring quest by the wizard Gandalf and thirteen dwarves to reclaim the Lonely Mountain and its treasure from the dragon Smaug.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg"
    },

    # Mystery, Thriller & Detective
    {
        "title": "The Da Vinci Code",
        "author": "Dan Brown",
        "genre": "Mystery & Thriller",
        "publication_year": 2003,
        "publisher": "Doubleday",
        "isbn": "9780307474278",
        "average_rating": 3.91,
        "rating_count": 2180000,
        "description": "Symbologist Robert Langdon investigates a murder in the Louvre Museum, uncovering cryptic clues in Leonardo da Vinci's paintings revealing an ancient secret society guarding the Holy Grail.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg"
    },
    {
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "genre": "Mystery & Thriller",
        "publication_year": 2012,
        "publisher": "Crown Publishing",
        "isbn": "9780307588371",
        "average_rating": 4.12,
        "rating_count": 2720000,
        "description": "On their fifth wedding anniversary, Nick Dunne reports his beautiful wife Amy missing. Under escalating media scrutiny and police suspicion, diaries and deceit expose dark secrets inside their toxic marriage.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307588371-L.jpg"
    },
    {
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "genre": "Mystery & Thriller",
        "publication_year": 2005,
        "publisher": "Norstedts Förlag",
        "isbn": "9780307949486",
        "average_rating": 4.16,
        "rating_count": 2980000,
        "description": "Journalist Mikael Blomkvist and genius hacker Lisbeth Salander unite to investigate the mysterious four-decade disappearance of Harriet Vanger from a wealthy Swedish industrial dynasty.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307949486-L.jpg"
    },
    {
        "title": "And Then There Were None",
        "author": "Agatha Christie",
        "genre": "Mystery & Thriller",
        "publication_year": 1939,
        "publisher": "Collins Crime Club",
        "isbn": "9780062073488",
        "average_rating": 4.28,
        "rating_count": 1250000,
        "description": "Ten strangers are lured to an isolated island mansion off the Devon coast by an eccentric host. One by one, each is murdered following the rhythm of a sinister nursery rhyme.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780062073488-L.jpg"
    },
    {
        "title": "The Silence of the Lambs",
        "author": "Thomas Harris",
        "genre": "Mystery & Thriller",
        "publication_year": 1988,
        "publisher": "St. Martin's Press",
        "isbn": "9780312924584",
        "average_rating": 4.24,
        "rating_count": 540000,
        "description": "FBI trainee Clarice Starling seeks the psychological profiling assistance of incarcerated cannibalistic serial killer Dr. Hannibal Lecter to track down an elusive murderer known as Buffalo Bill.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780312924584-L.jpg"
    },

    # Science, Philosophy & Psychology
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "genre": "Science & History",
        "publication_year": 2011,
        "publisher": "Harper",
        "isbn": "9780062316097",
        "average_rating": 4.36,
        "rating_count": 1390000,
        "description": "How did an insignificant ape become the ruler of planet Earth? Harari spans biology, anthropology, and economics to chart the cognitive, agricultural, and scientific revolutions shaping human destiny.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg"
    },
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "genre": "Science & Philosophy",
        "publication_year": 2011,
        "publisher": "Farrar, Straus and Giroux",
        "isbn": "9780374533557",
        "average_rating": 4.18,
        "rating_count": 520000,
        "description": "Nobel laureate Daniel Kahneman reveals the dual cognitive systems driving human thought: System 1 (fast, intuitive, emotional) and System 2 (slow, deliberate, analytical), analyzing cognitive biases and heuristics.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780374533557-L.jpg"
    },
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "genre": "Science & Philosophy",
        "publication_year": 1988,
        "publisher": "Bantam Books",
        "isbn": "9780553380163",
        "average_rating": 4.20,
        "rating_count": 480000,
        "description": "Stephen Hawking explores fundamental questions about the cosmos: How did the universe begin? What is time? Are black holes really black? A brilliant popular science masterpiece.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553380163-L.jpg"
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Psychology & Self-Help",
        "publication_year": 2018,
        "publisher": "Avery",
        "isbn": "9780735211292",
        "average_rating": 4.37,
        "rating_count": 1820000,
        "description": "An actionable framework based on behavioral psychology and neuroscience for forming good habits, breaking bad ones, and mastering tiny behaviors that lead to remarkable personal and professional transformations.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg"
    },
    {
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "genre": "Science & Philosophy",
        "publication_year": 180,
        "publisher": "Penguin Classics",
        "isbn": "9780140449334",
        "average_rating": 4.27,
        "rating_count": 280000,
        "description": "Personal spiritual writings of the Roman Emperor Marcus Aurelius, offering timeless Stoic philosophy on resilience, virtue, mindfulness, duty, and emotional calm amid chaos.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780140449334-L.jpg"
    },
    {
        "title": "Man's Search for Meaning",
        "author": "Viktor E. Frankl",
        "genre": "Psychology & Self-Help",
        "publication_year": 1946,
        "publisher": "Beacon Press",
        "isbn": "9780807014295",
        "average_rating": 4.37,
        "rating_count": 820000,
        "description": "Psychiatrist Viktor Frankl's memoir of surviving Nazi concentration camps and his development of logotherapy—the doctrine that humanity's primary motivational force is the quest for meaning in life.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780807014295-L.jpg"
    },
    {
        "title": "Cosmos",
        "author": "Carl Sagan",
        "genre": "Science & Philosophy",
        "publication_year": 1980,
        "publisher": "Random House",
        "isbn": "9780345539434",
        "average_rating": 4.40,
        "rating_count": 175000,
        "description": "Carl Sagan's poetic voyage across fifteen billion years of cosmic evolution, tracing the development of science, astronomy, galaxies, and human civilization's responsibility toward our pale blue dot.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780345539434-L.jpg"
    },

    # Classic Literature & Historical Fiction
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "Classic Literature",
        "publication_year": 1813,
        "publisher": "T. Egerton",
        "isbn": "9780141439518",
        "average_rating": 4.29,
        "rating_count": 3900000,
        "description": "The spirited Elizabeth Bennet navigates social status, family expectations, and romance in Regency England while sparring with the haughty and enigmatic Mr. Darcy.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg"
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic Literature",
        "publication_year": 1925,
        "publisher": "Charles Scribner's Sons",
        "isbn": "9780743273565",
        "average_rating": 3.93,
        "rating_count": 4700000,
        "description": "Narrated by Nick Carraway, this critique of the American Dream in the Roaring Twenties chronicles the lavish Long Island parties and obsessive love of the enigmatic millionaire Jay Gatsby for Daisy Buchanan.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg"
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Classic Literature",
        "publication_year": 1960,
        "publisher": "J. B. Lippincott & Co.",
        "isbn": "9780060935467",
        "average_rating": 4.26,
        "rating_count": 5500000,
        "description": "Through the eyes of young Scout Finch in Maycomb, Alabama, attorney Atticus Finch defends a Black man falsely accused of raping a white woman, confronting deep-seated prejudice and moral courage.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780060935467-L.jpg"
    },
    {
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "genre": "Classic Literature",
        "publication_year": 1866,
        "publisher": "The Russian Messenger",
        "isbn": "9780140449136",
        "average_rating": 4.25,
        "rating_count": 860000,
        "description": "Impoverished student Rodion Raskolnikov commits murder in Saint Petersburg believing he is an extraordinary individual above moral law, only to suffer agonizing psychological guilt and paranoia.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780140449136-L.jpg"
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "genre": "Classic Literature",
        "publication_year": 1951,
        "publisher": "Little, Brown and Company",
        "isbn": "9780316769488",
        "average_rating": 3.80,
        "rating_count": 3100000,
        "description": "Sixteen-year-old Holden Caulfield wanders New York City after being expelled from his prep school, railing against the phoniness of the adult world while searching for innocence and identity.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316769488-L.jpg"
    },
    {
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "genre": "Historical Fiction",
        "publication_year": 2005,
        "publisher": "Picador",
        "isbn": "9780375842207",
        "average_rating": 4.39,
        "rating_count": 2350000,
        "description": "Narrated by Death, the story follows Liesel Meminger, a young foster girl living near Munich in Nazi Germany who steals books to share with her neighbours and the Jewish fist-fighter hidden in her basement.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780375842207-L.jpg"
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": "Philosophy & Fiction",
        "publication_year": 1988,
        "publisher": "HarperTorch",
        "isbn": "9780061122415",
        "average_rating": 3.90,
        "rating_count": 2800000,
        "description": "Santiago, an Andalusian shepherd boy, dreams of discovering a worldly treasure buried near the Egyptian pyramids, journeying through the desert while learning to listen to his heart and pursue his Personal Legend.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780061122415-L.jpg"
    },
    {
        "title": "The Picture of Dorian Gray",
        "author": "Oscar Wilde",
        "genre": "Classic Literature",
        "publication_year": 1890,
        "publisher": "Ward, Lock and Company",
        "isbn": "9780141439570",
        "average_rating": 4.12,
        "rating_count": 1400000,
        "description": "A handsome young man sells his soul so that a painted portrait ages and bears the scars of his sins while he maintains eternal youth and hedonistic beauty in Victorian London.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780141439570-L.jpg"
    },
    {
        "title": "Frankenstein",
        "author": "Mary Shelley",
        "genre": "Science Fiction",
        "publication_year": 1818,
        "publisher": "Lackington, Hughes, Harding, Mavor & Jones",
        "isbn": "9780141439471",
        "average_rating": 3.86,
        "rating_count": 1500000,
        "description": "Obsessed young scientist Victor Frankenstein breathes life into a creature constructed from dead flesh, abandoning his creation in horror and provoking tragic revenge and philosophical ruin.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780141439471-L.jpg"
    },
    {
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "genre": "Historical Fiction",
        "publication_year": 2003,
        "publisher": "Riverhead Books",
        "isbn": "9781594631931",
        "average_rating": 4.34,
        "rating_count": 3100000,
        "description": "An unforgettable story of the unlikely friendship between Amir, the son of a wealthy merchant, and Hassan, the son of his father's servant, set against the tragic backdrop of Afghanistan's turmoil.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781594631931-L.jpg"
    },
    {
        "title": "Klara and the Sun",
        "author": "Kazuo Ishiguro",
        "genre": "Science Fiction",
        "publication_year": 2021,
        "publisher": "Faber and Faber",
        "isbn": "9780593318171",
        "average_rating": 3.79,
        "rating_count": 210000,
        "description": "Klara, an Artificial Friend with outstanding observational qualities, watches human behaviour from the shop window, hoping to be chosen by a child she can love and protect in a genetically stratified society.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780593318171-L.jpg"
    },
    {
        "title": "Clean Architecture: A Craftsman's Guide to Software Structure",
        "author": "Robert C. Martin",
        "genre": "Computer Science & AI",
        "publication_year": 2017,
        "publisher": "Prentice Hall",
        "isbn": "9780134494166",
        "average_rating": 4.31,
        "rating_count": 24000,
        "description": "Practical rules for software architecture and structural design. Uncle Bob explains SOLID principles, component boundaries, dependency inversion, and decoupling database and UI from business logic.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780134494166-L.jpg"
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt & David Thomas",
        "genre": "Computer Science & AI",
        "publication_year": 1999,
        "publisher": "Addison-Wesley",
        "isbn": "9780201616224",
        "average_rating": 4.33,
        "rating_count": 52000,
        "description": "Timeless wisdom on software craftsmanship, tackling everything from career development and personal responsibility to avoiding duplication (DRY), decoupling code, and writing flexible systems.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780201616224-L.jpg"
    },
    {
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "genre": "Biography & History",
        "publication_year": 2011,
        "publisher": "Simon & Schuster",
        "isbn": "9781451648539",
        "average_rating": 4.15,
        "rating_count": 1200000,
        "description": "Based on more than forty interviews with Jobs conducted over two years, Isaacson pens the gripping story of the roller-coaster life and searingly intense personality of a creative entrepreneur whose passion revolutionized six industries.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg"
    },
    {
        "title": "Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future",
        "author": "Ashlee Vance",
        "genre": "Biography & History",
        "publication_year": 2015,
        "publisher": "Ecco",
        "isbn": "9780062301239",
        "average_rating": 4.18,
        "rating_count": 310000,
        "description": "A comprehensive biography providing an intimate look into the life and work of Silicon Valley's most audacious entrepreneur, exploring the founding struggles of PayPal, Tesla Motors, and SpaceX.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780062301239-L.jpg"
    },
    {
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "genre": "Science & History",
        "publication_year": 1997,
        "publisher": "W. W. Norton & Company",
        "isbn": "9780393317558",
        "average_rating": 4.04,
        "rating_count": 380000,
        "description": "Pulitzer Prize-winning historical analysis demonstrating how geographical, environmental, and biogeographical factors—rather than racial or cultural superiority—shaped the modern human world.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780393317558-L.jpg"
    },
    {
        "title": "Zero to One: Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel & Blake Masters",
        "genre": "Business & Technology",
        "publication_year": 2014,
        "publisher": "Crown Business",
        "isbn": "9780804139298",
        "average_rating": 4.17,
        "rating_count": 320000,
        "description": "The legendary venture capitalist and PayPal co-founder outlines the philosophy that genuine innovation requires going from 0 to 1—creating new monopolies rather than competing in established commodity markets.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780804139298-L.jpg"
    },
    {
        "title": "The Lean Startup",
        "author": "Eric Ries",
        "genre": "Business & Technology",
        "publication_year": 2011,
        "publisher": "Crown Business",
        "isbn": "9780307887894",
        "average_rating": 4.11,
        "rating_count": 290000,
        "description": "How today's entrepreneurs use continuous innovation and validated learning through Build-Measure-Learn feedback loops and Minimum Viable Products to create radically successful businesses.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307887894-L.jpg"
    },
    {
        "title": "Hyperion",
        "author": "Dan Simmons",
        "genre": "Science Fiction",
        "publication_year": 1989,
        "publisher": "Doubleday",
        "isbn": "9780553283686",
        "average_rating": 4.24,
        "rating_count": 210000,
        "description": "On the eve of galactic war, seven pilgrims travel to the mysterious Time Tombs on the world of Hyperion, home to the dreadful metallic creature known as the Shrike. A Hugo Award-winning science fiction epic.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553283686-L.jpg"
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "genre": "Science Fiction",
        "publication_year": 2011,
        "publisher": "Crown Publishing",
        "isbn": "9780804139021",
        "average_rating": 4.41,
        "rating_count": 1150000,
        "description": "Astronaut Mark Watney is stranded on Mars after a fierce dust storm forces his crew to evacuate believing he died. Armed only with botanical knowledge, engineering ingenuity, and grit, he fights for survival.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780804139021-L.jpg"
    },
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "genre": "Science Fiction",
        "publication_year": 2021,
        "publisher": "Ballantine Books",
        "isbn": "9780593135204",
        "average_rating": 4.52,
        "rating_count": 620000,
        "description": "Ryland Grace is the sole survivor on a desperate last-chance interstellar mission to save humanity from an extraterrestrial microbe that is consuming the sun's energy, accompanied by an unexpected alien ally.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780593135204-L.jpg"
    },
    {
        "title": "Good to Great",
        "author": "Jim Collins",
        "genre": "Business & Technology",
        "publication_year": 2001,
        "publisher": "HarperBusiness",
        "isbn": "9780066620992",
        "average_rating": 4.13,
        "rating_count": 210000,
        "description": "Management study uncovering why some companies make the leap from average to enduring greatness while others fail, introducing the Hedgehog Concept, Level 5 Leadership, and the Flywheel effect.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780066620992-L.jpg"
    },
    {
        "title": "Atomic Habits: Companion Workbook",
        "author": "James Clear",
        "genre": "Psychology & Self-Help",
        "publication_year": 2020,
        "publisher": "Avery",
        "isbn": "9780593189641",
        "average_rating": 4.25,
        "rating_count": 35000,
        "description": "Practical worksheets, habit scorecards, and implementation intentions designed to accompany Atomic Habits for tracking daily behavioral feedback loops and compounding small lifestyle improvements.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg"
    },
    {
        "title": "Deep Work: Rules for Focused Success in a Distracted World",
        "author": "Cal Newport",
        "genre": "Psychology & Self-Help",
        "publication_year": 2016,
        "publisher": "Grand Central Publishing",
        "isbn": "9781455586691",
        "average_rating": 4.19,
        "rating_count": 180000,
        "description": "Computer science professor Cal Newport argues that deep work—the ability to focus without distraction on cognitively demanding tasks—is a rare superpower that produces peak creative value in the information economy.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781455586691-L.jpg"
    },
    {
        "title": "Show Your Work!",
        "author": "Austin Kleon",
        "genre": "Psychology & Self-Help",
        "publication_year": 2014,
        "publisher": "Workman Publishing",
        "isbn": "9780761178972",
        "average_rating": 4.18,
        "rating_count": 130000,
        "description": "Ten ways to share your creativity and get discovered. An inspiring manifesto on being an amateur, sharing daily scraps of learning, and building a generous network instead of traditional networking.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780761178972-L.jpg"
    },
    {
        "title": "Steal Like an Artist",
        "author": "Austin Kleon",
        "genre": "Psychology & Self-Help",
        "publication_year": 2012,
        "publisher": "Workman Publishing",
        "isbn": "9780761169253",
        "average_rating": 3.92,
        "rating_count": 220000,
        "description": "Nothing is completely original: all creative work builds on what came before. Kleon delivers an inspiring visual handbook on embracing influences, remixing ideas, and finding your artistic voice.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780761169253-L.jpg"
    },
    {
        "title": "Quiet: The Power of Introverts in a World That Can't Stop Talking",
        "author": "Susan Cain",
        "genre": "Psychology & Self-Help",
        "publication_year": 2012,
        "publisher": "Crown Publishing",
        "isbn": "9780307352149",
        "average_rating": 4.08,
        "rating_count": 480000,
        "description": "At least one-third of the people we know are introverts. Susan Cain investigates neurological differences and challenges cultural biases toward extroverts, demonstrating how deep thinkers transform science and culture.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307352149-L.jpg"
    },
    {
        "title": "Start with Why",
        "author": "Simon Sinek",
        "genre": "Business & Technology",
        "publication_year": 2009,
        "publisher": "Portfolio",
        "isbn": "9781591846444",
        "average_rating": 4.09,
        "rating_count": 240000,
        "description": "Simon Sinek discovers that leaders who have had the greatest influence in the world all think, act, and communicate the exact same way—starting with 'Why', the core purpose and emotional cause behind action.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781591846444-L.jpg"
    },
    {
        "title": "Thinking in Systems: A Primer",
        "author": "Donella H. Meadows",
        "genre": "Science & Philosophy",
        "publication_year": 2008,
        "publisher": "Chelsea Green Publishing",
        "isbn": "9781603580557",
        "average_rating": 4.29,
        "rating_count": 45000,
        "description": "An essential guide to systems thinking, feedback loops, stocks, and flows, teaching how to recognize non-linear dynamics and solve complex organizational, social, and ecological dilemmas.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781603580557-L.jpg"
    },
    {
        "title": "Grokking Algorithms",
        "author": "Aditya Y. Bhargava",
        "genre": "Computer Science & AI",
        "publication_year": 2016,
        "publisher": "Manning Publications",
        "isbn": "9781617292231",
        "average_rating": 4.54,
        "rating_count": 18000,
        "description": "A fully illustrated, friendly guide that teaches how to apply common algorithms to practical problems. Covers binary search, recursion, quicksort, graph algorithms, Dijkstra's algorithm, and greedy approaches.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781617292231-L.jpg"
    },
    {
        "title": "The Road",
        "author": "Cormac McCarthy",
        "genre": "Dystopian Fiction",
        "publication_year": 2006,
        "publisher": "Alfred A. Knopf",
        "isbn": "9780307387899",
        "average_rating": 3.99,
        "rating_count": 890000,
        "description": "A father and his young son walk alone through burned post-apocalyptic America toward the coast, sustaining each other with fierce love amidst ash, starvation, and ruthless marauders. Pulitzer Prize winner.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307387899-L.jpg"
    },
    {
        "title": "Educated: A Memoir",
        "author": "Tara Westover",
        "genre": "Biography & History",
        "publication_year": 2018,
        "publisher": "Random House",
        "isbn": "9780399590504",
        "average_rating": 4.47,
        "rating_count": 1350000,
        "description": "Born to survivalist parents in rural Idaho, Tara Westover was isolated from mainstream society with no birth certificate or formal schooling. She taught herself mathematics and grammar, eventually earning a PhD from Cambridge.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780399590504-L.jpg"
    },
    {
        "title": "When Breath Becomes Air",
        "author": "Paul Kalanithi",
        "genre": "Biography & History",
        "publication_year": 2016,
        "publisher": "Random House",
        "isbn": "9780812988406",
        "average_rating": 4.39,
        "rating_count": 720000,
        "description": "At age thirty-six, on the verge of completing a decade of training as a neurosurgeon, Paul Kalanithi was diagnosed with stage IV lung cancer. A profound reflection on mortality and finding meaning in life.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780812988406-L.jpg"
    },
    {
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "genre": "Science Fiction",
        "publication_year": 1979,
        "publisher": "Pan Books",
        "isbn": "9780345391803",
        "average_rating": 4.23,
        "rating_count": 1650000,
        "description": "Seconds before Earth is demolished by a Vogon constructor fleet to make way for a hyperspace bypass, Arthur Dent is plucked off the planet by his friend Ford Prefect, a researcher for the titular electronic guide.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780345391803-L.jpg"
    },
    {
        "title": "The Code Breaker: Jennifer Doudna, Gene Editing, and the Future of the Human Race",
        "author": "Walter Isaacson",
        "genre": "Science & History",
        "publication_year": 2021,
        "publisher": "Simon & Schuster",
        "isbn": "9781982115852",
        "average_rating": 4.28,
        "rating_count": 110000,
        "description": "The story of Nobel Prize-winning scientist Jennifer Doudna and her colleagues who developed CRISPR gene-editing technology, unlocking the power to cure diseases, ward off viruses, and edit human genetics.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781982115852-L.jpg"
    },
    {
        "title": "Weapons of Math Destruction: How Big Data Increases Inequality and Threatens Democracy",
        "author": "Cathy O'Neil",
        "genre": "Computer Science & AI",
        "publication_year": 2016,
        "publisher": "Crown Publishing",
        "isbn": "9780553418811",
        "average_rating": 3.86,
        "rating_count": 38000,
        "description": "Mathematician Cathy O'Neil exposes how unregulated black-box machine-learning algorithms in credit scoring, policing, hiring, and insurance reinforce racial and socioeconomic discrimination.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553418811-L.jpg"
    },
    {
        "title": "The Alignment Problem: Machine Learning and Human Values",
        "author": "Brian Christian",
        "genre": "Computer Science & AI",
        "publication_year": 2020,
        "publisher": "W. W. Norton & Company",
        "isbn": "9780393635829",
        "average_rating": 4.38,
        "rating_count": 16000,
        "description": "An investigation into the technical challenges of ensuring artificial intelligence systems understand and uphold human values, covering algorithmic fairness, reinforcement learning from human feedback, and transparency.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780393635829-L.jpg"
    },
    {
        "title": "The Innovators: How a Group of Hackers, Geniuses, and Geeks Created the Digital Revolution",
        "author": "Walter Isaacson",
        "genre": "Computer Science & AI",
        "publication_year": 2014,
        "publisher": "Simon & Schuster",
        "isbn": "9781476708690",
        "average_rating": 4.14,
        "rating_count": 89000,
        "description": "Beginning with Ada Lovelace, Lord Byron's daughter who pioneered computer programming in the 1840s, Isaacson traces the collaborative genius that produced transistors, the microchip, personal computers, and the internet.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781476708690-L.jpg"
    },
    {
        "title": "Siddhartha",
        "author": "Hermann Hesse",
        "genre": "Philosophy & Fiction",
        "publication_year": 1922,
        "publisher": "S. Fischer Verlag",
        "isbn": "9780553208849",
        "average_rating": 4.07,
        "rating_count": 720000,
        "description": "In ancient India, young Brahmin Siddhartha embarks on a spiritual quest, leaving behind ascetic wandering, worldly pleasure, and wealth to find inner enlightenment listening to the tranquil river.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553208849-L.jpg"
    },
    {
        "title": "Norwegian Wood",
        "author": "Haruki Murakami",
        "genre": "Classic Literature",
        "publication_year": 1987,
        "publisher": "Kodansha",
        "isbn": "9780375704024",
        "average_rating": 4.02,
        "rating_count": 480000,
        "description": "Toru Watanabe recalls his college days in late 1960s Tokyo, navigating loss, grief, and love caught between the emotionally fragile Naoko and the vibrant, independent Midori.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780375704024-L.jpg"
    },
    {
        "title": "Kafka on the Shore",
        "author": "Haruki Murakami",
        "genre": "Fantasy",
        "publication_year": 2002,
        "publisher": "Shinchosha",
        "isbn": "9781400079278",
        "average_rating": 4.14,
        "rating_count": 390000,
        "description": "A teenage runaway named Kafka Tamura and an aging, simple man named Nakata who can converse with cats embark on parallel metaphysical journeys interlaced with magical realism and psychological riddles.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781400079278-L.jpg"
    },
    {
        "title": "The Metamorphosis",
        "author": "Franz Kafka",
        "genre": "Classic Literature",
        "publication_year": 1915,
        "publisher": "Kurt Wolff Verlag",
        "isbn": "9780143105244",
        "average_rating": 3.84,
        "rating_count": 820000,
        "description": "Traveling salesman Gregor Samsa awakens one morning transformed into a monstrous insect, struggling to adapt while observing his family's horror, resentment, and eventual alienation.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780143105244-L.jpg"
    },
    {
        "title": "The Stranger",
        "author": "Albert Camus",
        "genre": "Science & Philosophy",
        "publication_year": 1942,
        "publisher": "Éditions Gallimard",
        "isbn": "9780679720201",
        "average_rating": 4.02,
        "rating_count": 910000,
        "description": "Through the detached character of Meursault, who attends his mother's funeral without weeping and kills a man on a sun-drenched Algerian beach, Camus explores the philosophy of the Absurd and societal conformity.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780679720201-L.jpg"
    },
    {
        "title": "The Myth of Sisyphus",
        "author": "Albert Camus",
        "genre": "Science & Philosophy",
        "publication_year": 1942,
        "publisher": "Éditions Gallimard",
        "isbn": "9780679733737",
        "average_rating": 4.18,
        "rating_count": 130000,
        "description": "One of the clearest philosophical expositions of existential absurdism: the confrontation between the human desire for purpose and the cold indifference of the universe. One must imagine Sisyphus happy.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780679733737-L.jpg"
    },
    {
        "title": "Slaughterhouse-Five",
        "author": "Kurt Vonnegut",
        "genre": "Science Fiction",
        "publication_year": 1969,
        "publisher": "Delacorte",
        "isbn": "9780440180296",
        "average_rating": 4.10,
        "rating_count": 1350000,
        "description": "Billy Pilgrim has become unstuck in time, traveling between his survival of the firebombing of Dresden in World War II, his post-war suburban life, and his display in an alien zoo on Tralfamadore.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780440180296-L.jpg"
    },
    {
        "title": "Cat's Cradle",
        "author": "Kurt Vonnegut",
        "genre": "Science Fiction",
        "publication_year": 1963,
        "publisher": "Holt, Rinehart and Winston",
        "isbn": "9780385333481",
        "average_rating": 4.18,
        "rating_count": 410000,
        "description": "A satirical commentary on the arms race and human folly centering on Ice-Nine, a deadly crystalline form of water capable of freezing all oceans, and the mock-religion Bokononism.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780385333481-L.jpg"
    },
    {
        "title": "The Cyberiad: Fables for the Cybernetic Age",
        "author": "Stanislaw Lem",
        "genre": "Science Fiction",
        "publication_year": 1965,
        "publisher": "Wydawnictwo Literackie",
        "isbn": "9780156027595",
        "average_rating": 4.26,
        "rating_count": 32000,
        "description": "Brilliant philosophical satire following Trurl and Klapaucius, two 'constructors' capable of building machines of extraordinary cosmic complexity, exploring artificial sentience, poetry machines, and universal harmony.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780156027595-L.jpg"
    },
    {
        "title": "Solaris",
        "author": "Stanislaw Lem",
        "genre": "Science Fiction",
        "publication_year": 1961,
        "publisher": "Wydawnictwo Ministerstwa Obrony Narodowej",
        "isbn": "9780156027601",
        "average_rating": 4.02,
        "rating_count": 125000,
        "description": "Kris Kelvin arrives at the research station above the oceanic planet Solaris to find the crew hallucinating painful manifestations of their subconscious memories created by the enigmatic living ocean.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780156027601-L.jpg"
    },
    {
        "title": "Gödel, Escher, Bach: An Eternal Golden Braid",
        "author": "Douglas Hofstadter",
        "genre": "Computer Science & AI",
        "publication_year": 1979,
        "publisher": "Basic Books",
        "isbn": "9780465026562",
        "average_rating": 4.30,
        "rating_count": 54000,
        "description": "Pulitzer Prize-winning exploration of how self-reference and strange loops in Kurt Gödel's incompleteness theorems, M.C. Escher's illusions, and J.S. Bach's fugues mirror how cognition and consciousness emerge from neurons.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780465026562-L.jpg"
    },
    {
        "title": "Pattern Recognition",
        "author": "William Gibson",
        "genre": "Science Fiction",
        "publication_year": 2003,
        "publisher": "G. P. Putnam's Sons",
        "isbn": "9780425192931",
        "average_rating": 3.84,
        "rating_count": 92000,
        "description": "Cayce Pollard, a coolhunter allergic to commercial branding, is hired to investigate the origin of mysterious, haunting video clips anonymously posted to internet forums around the globe.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780425192931-L.jpg"
    },
    {
        "title": "The Diamond Age: Or, A Young Lady's Illustrated Primer",
        "author": "Neal Stephenson",
        "genre": "Science Fiction",
        "publication_year": 1995,
        "publisher": "Bantam Spectra",
        "isbn": "9780553380965",
        "average_rating": 4.16,
        "rating_count": 110000,
        "description": "In a post-scarcity future dominated by nanotechnology and tribal phyles, an impoverished young girl named Nell receives an illicit interactive artificial intelligence primer that guides her education and destiny.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553380965-L.jpg"
    },
    {
        "title": "Cryptonomicon",
        "author": "Neal Stephenson",
        "genre": "Science Fiction",
        "publication_year": 1999,
        "publisher": "Avon",
        "isbn": "9780060512804",
        "average_rating": 4.25,
        "rating_count": 120000,
        "description": "A dual narrative weaving World War II Allied codebreakers alongside Alan Turing with 1990s cypherpunks building an anonymous data haven in Southeast Asia.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780060512804-L.jpg"
    },
    {
        "title": "Ready Player One",
        "author": "Ernest Cline",
        "genre": "Science Fiction",
        "publication_year": 2011,
        "publisher": "Crown Publishing",
        "isbn": "9780307887436",
        "average_rating": 4.23,
        "rating_count": 1150000,
        "description": "In a bleak 2045, teenager Wade Watts escapes reality inside the OASIS, an expansive virtual universe. When its eccentric creator dies leaving his fortunes to the first person to find a hidden Easter egg, an epic treasure hunt begins.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780307887436-L.jpg"
    },
    {
        "title": "Ender's Game",
        "author": "Orson Scott Card",
        "genre": "Science Fiction",
        "publication_year": 1985,
        "publisher": "Tor Books",
        "isbn": "9780812550702",
        "average_rating": 4.31,
        "rating_count": 1300000,
        "description": "Ender Wiggin, a quiet child prodigy, is recruited into an elite orbital Battle School to train in zero-gravity strategic warfare against an imminent extraterrestrial insectoid invasion.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780812550702-L.jpg"
    },
    {
        "title": "Speaker for the Dead",
        "author": "Orson Scott Card",
        "genre": "Science Fiction",
        "publication_year": 1986,
        "publisher": "Tor Books",
        "isbn": "9780812550757",
        "average_rating": 4.09,
        "rating_count": 250000,
        "description": "Three thousand years after the Xenocide, Ender journeys to the colony world of Lusitania as a Speaker for the Dead to investigate the brutal murder of scientists by a newly discovered intelligent species known as the Piggies.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780812550757-L.jpg"
    },
    {
        "title": "The Dispossessed",
        "author": "Ursula K. Le Guin",
        "genre": "Science Fiction",
        "publication_year": 1974,
        "publisher": "Harper & Row",
        "isbn": "9780060512750",
        "average_rating": 4.24,
        "rating_count": 135000,
        "description": "Physicist Shevek travels from the anarcho-syndicalist moon of Anarres to the decadent capitalist mother world Urras to share his General Temporal Theory, discovering the limitations of both utopias.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780060512750-L.jpg"
    },
    {
        "title": "Earthsea: A Wizard of Earthsea",
        "author": "Ursula K. Le Guin",
        "genre": "Fantasy",
        "publication_year": 1968,
        "publisher": "Parnassus Press",
        "isbn": "9780547722023",
        "average_rating": 4.01,
        "rating_count": 310000,
        "description": "Young wizard Ged, nicknamed Sparrowhawk, lets pride unleash a terrifying shadow beast into the archipelago of Earthsea. He must voyage across the uncharted oceans to confront his own darkness.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547722023-L.jpg"
    },
    {
        "title": "I, Robot",
        "author": "Isaac Asimov",
        "genre": "Science Fiction",
        "publication_year": 1950,
        "publisher": "Gnome Press",
        "isbn": "9780553382562",
        "average_rating": 4.21,
        "rating_count": 380000,
        "description": "Robopsychologist Dr. Susan Calvin recounts the history of human-robot development and the ethical paradoxes emerging under the Three Laws of Robotics.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553382562-L.jpg"
    },
    {
        "title": "The Caves of Steel",
        "author": "Isaac Asimov",
        "genre": "Science Fiction",
        "publication_year": 1954,
        "publisher": "Doubleday",
        "isbn": "9780553288285",
        "average_rating": 4.18,
        "rating_count": 120000,
        "description": "A murder mystery set in enclosed underground mega-cities of Earth. Detective Elijah Baley is reluctantly partnered with R. Daneel Olivaw, a sophisticated humanoid robot, to solve a politically sensitive assassination.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553288285-L.jpg"
    },
    {
        "title": "Second Foundation",
        "author": "Isaac Asimov",
        "genre": "Science Fiction",
        "publication_year": 1953,
        "publisher": "Gnome Press",
        "isbn": "9780553293364",
        "average_rating": 4.25,
        "rating_count": 185000,
        "description": "As the mutant telepath known as the Mule threatens the Seldon Plan, the First Foundation desperately searches for the mysterious, hidden Second Foundation of mentalics tasked with guarding humanity's psychology.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553293364-L.jpg"
    },
    {
        "title": "Children of Time",
        "author": "Adrian Tchaikovsky",
        "genre": "Science Fiction",
        "publication_year": 2015,
        "publisher": "Tor Books",
        "isbn": "9780316452502",
        "average_rating": 4.30,
        "rating_count": 120000,
        "description": "The last remnants of humanity flee a ruined Earth on an ark ship, heading towards a terraformed planet where an accelerated nanovirus has instead evolved a complex, sentient civilization of portia spiders.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316452502-L.jpg"
    },
    {
        "title": "Recursion",
        "author": "Blake Crouch",
        "genre": "Science Fiction",
        "publication_year": 2019,
        "publisher": "Crown Publishing",
        "isbn": "9781524759780",
        "average_rating": 4.16,
        "rating_count": 190000,
        "description": "A neuroscientist invents technology intended to preserve cherished memories for Alzheimer's patients, unwittingly unleashing False Memory Syndrome and enabling the rewrite of reality itself.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781524759780-L.jpg"
    },
    {
        "title": "Dark Matter",
        "author": "Blake Crouch",
        "genre": "Science Fiction",
        "publication_year": 2016,
        "publisher": "Crown Publishing",
        "isbn": "9781101945957",
        "average_rating": 4.13,
        "rating_count": 410000,
        "description": "College physics professor Jason Dessen is kidnapped, knocked unconscious, and wakes up in a quantum research lab where his wife is not his wife, his son was never born, and he is a celebrated genius who built a portal into the multiverse.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781101945957-L.jpg"
    },
    {
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "genre": "Philosophy & Fiction",
        "publication_year": 2020,
        "publisher": "Viking",
        "isbn": "9780525559474",
        "average_rating": 4.02,
        "rating_count": 1600000,
        "description": "Between life and death lies a library filled with infinite books, each representing a life Nora Seed could have lived had she made different choices. She gets the chance to undo regrets and find what makes life truly fulfilling.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780525559474-L.jpg"
    },
    {
        "title": "The Song of Achilles",
        "author": "Madeline Miller",
        "genre": "Historical Fiction",
        "publication_year": 2011,
        "publisher": "Ecco",
        "isbn": "9780062060624",
        "average_rating": 4.33,
        "rating_count": 1500000,
        "description": "A lyrical reimagining of the Iliad depicting the deep bond and tragic love between the awkward exiled prince Patroclus and the golden hero Achilles during the Trojan War.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780062060624-L.jpg"
    },
    {
        "title": "Circe",
        "author": "Madeline Miller",
        "genre": "Fantasy",
        "publication_year": 2018,
        "publisher": "Little, Brown and Company",
        "isbn": "9780316556347",
        "average_rating": 4.25,
        "rating_count": 1050000,
        "description": "In the house of Helios, god of the sun, a strange child named Circe discovers her power of witchcraft. Banished to a deserted island, she hones her occult craft, defying gods and protecting what she loves.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316556347-L.jpg"
    },
    {
        "title": "Project Phoenix: Building Resilient Systems",
        "author": "Gene Kim, Kevin Behr, George Spafford",
        "genre": "Computer Science & AI",
        "publication_year": 2013,
        "publisher": "IT Revolution Press",
        "isbn": "9780988262591",
        "average_rating": 4.27,
        "rating_count": 68000,
        "description": "A novel about IT, DevOps, and helping your business win. An IT manager has ninety days to rescue an overdue mission-critical payroll project using Three Ways of agile flow, feedback loops, and continual experimentation.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780988262591-L.jpg"
    },
    {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "genre": "Computer Science & AI",
        "publication_year": 2009,
        "publisher": "MIT Press",
        "isbn": "9780262033848",
        "average_rating": 4.35,
        "rating_count": 48000,
        "description": "The quintessential 'CLRS' textbook providing rigorous proofs, pseudocode, and mathematical analysis for sorting, dynamic programming, greedy algorithms, advanced data structures, graph theory, and NP-completeness.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780262033848-L.jpg"
    },
    {
        "title": "Linear Algebra Done Right",
        "author": "Sheldon Axler",
        "genre": "Science & Philosophy",
        "publication_year": 2015,
        "publisher": "Springer",
        "isbn": "9783319110790",
        "average_rating": 4.45,
        "rating_count": 12000,
        "description": "A pure, determinant-free approach to linear algebra focusing on linear operators on finite-dimensional vector spaces, eigenvalues, eigenvectors, and inner-product spaces—essential mathematics for machine learning.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9783319110790-L.jpg"
    },
    {
        "title": "Mathematics for Machine Learning",
        "author": "Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong",
        "genre": "Computer Science & AI",
        "publication_year": 2020,
        "publisher": "Cambridge University Press",
        "isbn": "9781108455145",
        "average_rating": 4.58,
        "rating_count": 8900,
        "description": "The fundamental mathematical toolkit for machine learning: linear algebra, analytic geometry, matrix decompositions, vector calculus, probability, and distribution theory applied to linear regression, PCA, and SVMs.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781108455145-L.jpg"
    },
    {
        "title": "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
        "author": "Aurélien Géron",
        "genre": "Computer Science & AI",
        "publication_year": 2022,
        "publisher": "O'Reilly Media",
        "isbn": "9781098125974",
        "average_rating": 4.71,
        "rating_count": 19500,
        "description": "Through concrete examples, minimal theory, and production-ready Python frameworks, Géron teaches practitioners how to build predictive ML systems, end-to-end data pipelines, transformers, and deep neural nets.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781098125974-L.jpg"
    },
    {
        "title": "Building Machine Learning Powered Applications",
        "author": "Emmanuel Ameisen",
        "genre": "Computer Science & AI",
        "publication_year": 2020,
        "publisher": "O'Reilly Media",
        "isbn": "9781492045113",
        "average_rating": 4.46,
        "rating_count": 4200,
        "description": "A practical guide to designing, prototyping, deploying, and evaluating machine learning applications in production. Emphasizes establishing heuristics, metric selection, error analysis, and iterative improvement.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781492045113-L.jpg"
    },
    {
        "title": "Natural Language Processing with Transformers",
        "author": "Lewis Tunstall, Leandro von Werra, Thomas Wolf",
        "genre": "Computer Science & AI",
        "publication_year": 2022,
        "publisher": "O'Reilly Media",
        "isbn": "9781098103248",
        "average_rating": 4.67,
        "rating_count": 5100,
        "description": "Written by core Hugging Face developers, this comprehensive handbook shows how to build, train, and scale state-of-the-art transformer models (BERT, GPT, T5) for classification, question answering, and text generation.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781098103248-L.jpg"
    },
    {
        "title": "The Elements of Statistical Learning",
        "author": "Trevor Hastie, Robert Tibshirani, Jerome Friedman",
        "genre": "Computer Science & AI",
        "publication_year": 2009,
        "publisher": "Springer",
        "isbn": "9780387848570",
        "average_rating": 4.49,
        "rating_count": 18000,
        "description": "A landmark theoretical treatise on statistical learning and data mining, covering boosting, random forests, support vector machines, neural networks, kernel smoothing, and high-dimensional inference.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780387848570-L.jpg"
    },
    {
        "title": "Pattern Recognition and Machine Learning",
        "author": "Christopher M. Bishop",
        "genre": "Computer Science & AI",
        "publication_year": 2006,
        "publisher": "Springer",
        "isbn": "9780387310732",
        "average_rating": 4.42,
        "rating_count": 14000,
        "description": "The first textbook on machine learning to present a comprehensive Bayesian viewpoint, covering graphical models, approximate inference, Markov random fields, and expectation maximization.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780387310732-L.jpg"
    },
    {
        "title": "Recommender Systems Handbook",
        "author": "Francesco Ricci, Lior Rokach, Bracha Shapira",
        "genre": "Computer Science & AI",
        "publication_year": 2015,
        "publisher": "Springer",
        "isbn": "9781489976369",
        "average_rating": 4.50,
        "rating_count": 2100,
        "description": "The authoritative academic handbook on modern recommender systems, detailing collaborative filtering, matrix factorization, content-based recommendation, hybrid algorithms, and offline evaluation protocols.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781489976369-L.jpg"
    },
    {
        "title": "Practical Recommender Systems",
        "author": "Kim Falk",
        "genre": "Computer Science & AI",
        "publication_year": 2019,
        "publisher": "Manning Publications",
        "isbn": "9781617292705",
        "average_rating": 4.38,
        "rating_count": 1900,
        "description": "Hands-on guide to building production recommendation engines using Python. Covers collaborative filtering, similarity metrics, cold-start strategies, non-personalized ranking, and live A/B evaluation.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781617292705-L.jpg"
    },
    {
        "title": "Mining of Massive Datasets",
        "author": "Jure Leskovec, Anand Rajaraman, Jeffrey D. Ullman",
        "genre": "Computer Science & AI",
        "publication_year": 2014,
        "publisher": "Cambridge University Press",
        "isbn": "9781107077232",
        "average_rating": 4.33,
        "rating_count": 6800,
        "description": "Focuses on algorithms for mining massive data: MapReduce, Locality-Sensitive Hashing, PageRank, stream computing, recommendation systems, and large-scale graph analysis.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781107077232-L.jpg"
    },
    {
        "title": "We",
        "author": "Yevgeny Zamyatin",
        "genre": "Dystopian Fiction",
        "publication_year": 1924,
        "publisher": "E.P. Dutton",
        "isbn": "9780140185850",
        "average_rating": 3.93,
        "rating_count": 92000,
        "description": "The grandfather of modern dystopian fiction. In the glass city of the One State, citizens are designated by numbers and governed by the Benefactor, until engineer D-503 falls in love and discovers rebellion.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780140185850-L.jpg"
    },
    {
        "title": "A Scanner Darkly",
        "author": "Philip K. Dick",
        "genre": "Science Fiction",
        "publication_year": 1977,
        "publisher": "Doubleday",
        "isbn": "9780547572178",
        "average_rating": 4.02,
        "rating_count": 115000,
        "description": "Undercover narcotics agent Bob Arctor is hooked on Substance D, a reality-altering drug that causes dual brain hemispheres to perceive each other as alien adversaries, eventually ordered to place surveillance on himself.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547572178-L.jpg"
    },
    {
        "title": "Ubik",
        "author": "Philip K. Dick",
        "genre": "Science Fiction",
        "publication_year": 1969,
        "publisher": "Doubleday",
        "isbn": "9780547572291",
        "average_rating": 4.08,
        "rating_count": 140000,
        "description": "Anti-telepathic agent Joe Chip investigates a sabotage bomb on the moon, only to find the fabric of space and time regressing into 1939 while a mysterious spray-can product called Ubik holds the antidote to cosmic decay.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547572291-L.jpg"
    },
    {
        "title": "The Man in the High Castle",
        "author": "Philip K. Dick",
        "genre": "Science Fiction",
        "publication_year": 1962,
        "publisher": "G. P. Putnam's Sons",
        "isbn": "9780547572482",
        "average_rating": 3.82,
        "rating_count": 260000,
        "description": "In an alternate 1962 where the Axis powers won World War II and partitioned the United States, characters consult the I Ching while passing around a banned novel describing an alternate world where the Allies triumphed.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547572482-L.jpg"
    },
    {
        "title": "Valis",
        "author": "Philip K. Dick",
        "genre": "Science Fiction",
        "publication_year": 1981,
        "publisher": "Bantam Books",
        "isbn": "9780547572413",
        "average_rating": 3.90,
        "rating_count": 48000,
        "description": "A semi-autobiographical theological science-fiction novel exploring Gnostic mysticism, mental illness, and communication with VALIS—a Vast Active Living Intelligence System beaming pink laser transmissions into human brains.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780547572413-L.jpg"
    },
    {
        "title": "Permutation City",
        "author": "Greg Egan",
        "genre": "Science Fiction",
        "publication_year": 1994,
        "publisher": "Millennium",
        "isbn": "9781597805391",
        "average_rating": 4.10,
        "rating_count": 18000,
        "description": "Paul Durham creates an artificial reality called the Autoverse where digital copies of human consciousness live, constructing a mathematical cellular automaton universe independent of physical reality.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781597805391-L.jpg"
    },
    {
        "title": "Diaspora",
        "author": "Greg Egan",
        "genre": "Science Fiction",
        "publication_year": 1997,
        "publisher": "Orion",
        "isbn": "9781597805407",
        "average_rating": 4.14,
        "rating_count": 16000,
        "description": "In the 30th century, humanity has bifurcated into fleshmers, gleisner robots, and digital polis citizens. An unexpected collision of binary neutron stars prompts a cosmic expedition across higher mathematical dimensions.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781597805407-L.jpg"
    },
    {
        "title": "Stories of Your Life and Others",
        "author": "Ted Chiang",
        "genre": "Science Fiction",
        "publication_year": 2002,
        "publisher": "Tor Books",
        "isbn": "9781101972120",
        "average_rating": 4.29,
        "rating_count": 140000,
        "description": "A collection of mind-bending philosophical science-fiction novellas, including 'Story of Your Life' (the basis for the film Arrival), exploring non-linear time, linguistics, determinism, and the nature of beauty.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781101972120-L.jpg"
    },
    {
        "title": "Exhalation: Stories",
        "author": "Ted Chiang",
        "genre": "Science Fiction",
        "publication_year": 2019,
        "publisher": "Knopf",
        "isbn": "9781101947883",
        "average_rating": 4.28,
        "rating_count": 165000,
        "description": "Nine sublime short stories addressing big existential questions: entropy, time travel, digital pets with consciousness, memory recording lenses, and free will in the multiverse.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781101947883-L.jpg"
    },
    {
        "title": "Blindsight",
        "author": "Peter Watts",
        "genre": "Science Fiction",
        "publication_year": 2006,
        "publisher": "Tor Books",
        "isbn": "9780765319647",
        "average_rating": 4.02,
        "rating_count": 42000,
        "description": "A crew of transhuman specialists—including a synthetically reconstructed vampire commander—is dispatched to the edge of the solar system to contact an alien artifact, raising the horrifying possibility that human consciousness is an evolutionary defect.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765319647-L.jpg"
    },
    {
        "title": "Roadside Picnic",
        "author": "Arkady and Boris Strugatsky",
        "genre": "Science Fiction",
        "publication_year": 1972,
        "publisher": "Macmillan",
        "isbn": "9781613743416",
        "average_rating": 4.14,
        "rating_count": 52000,
        "description": "Extraterrestrials briefly visited Earth and departed leaving behind the Zone—a radioactive, anomaly-filled wasteland strewn with dangerous alien trash. 'Stalker' Red Schuhart risks his life scavenging its lethal artifacts.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781613743416-L.jpg"
    },
    {
        "title": "Solaris and Other Stories",
        "author": "Stanislaw Lem",
        "genre": "Science Fiction",
        "publication_year": 1968,
        "publisher": "Penguin Classics",
        "isbn": "9780141198538",
        "average_rating": 4.12,
        "rating_count": 31000,
        "description": "Essential tales of contact with genuinely incomprehensible extraterrestrial minds, challenging human anthropocentrism and the limits of scientific observation.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780141198538-L.jpg"
    },
    {
        "title": "The Player of Games",
        "author": "Iain M. Banks",
        "genre": "Science Fiction",
        "publication_year": 1988,
        "publisher": "Macmillan",
        "isbn": "9780316005401",
        "average_rating": 4.25,
        "rating_count": 89000,
        "description": "Jernau Morat Gurgeh, a master game player in the post-scarcity utopian civilization of the Culture, is recruited by Special Circumstances to travel to the brutal Empire of Azad and play its complex socio-political game.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316005401-L.jpg"
    },
    {
        "title": "Use of Weapons",
        "author": "Iain M. Banks",
        "genre": "Science Fiction",
        "publication_year": 1990,
        "publisher": "Orbit",
        "isbn": "9780316005388",
        "average_rating": 4.19,
        "rating_count": 62000,
        "description": "Told in alternating chronological and reverse-chronological chapters, this Culture novel centers on Cheradenine Zakalwe, a mercenary operative haunted by the unspeakable atrocity of the Chairmaker.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316005388-L.jpg"
    },
    {
        "title": "Look to Windward",
        "author": "Iain M. Banks",
        "genre": "Science Fiction",
        "publication_year": 2000,
        "publisher": "Orbit",
        "isbn": "9780316005425",
        "average_rating": 4.22,
        "rating_count": 48000,
        "description": "Eight hundred years after the Idiran War, the light from two stellar supernovas reaches the Culture Orbital Masaq', where a renegade composer plots revenge for a war-time genocide.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316005425-L.jpg"
    },
    {
        "title": "Annihilation",
        "author": "Jeff VanderMeer",
        "genre": "Science Fiction",
        "publication_year": 2014,
        "publisher": "FSG Originals",
        "isbn": "9780374104092",
        "average_rating": 3.74,
        "rating_count": 310000,
        "description": "A female biologist joins the twelfth expedition into Area X, an isolated coastal zone where nature has transformed into eerie, mutating ecosystems that swallow human expeditions.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780374104092-L.jpg"
    },
    {
        "title": "Red Mars",
        "author": "Kim Stanley Robinson",
        "genre": "Science Fiction",
        "publication_year": 1992,
        "publisher": "Bantam Spectra",
        "isbn": "9780553560732",
        "average_rating": 3.86,
        "rating_count": 89000,
        "description": "The first contingent of one hundred colonists arrives on Mars to establish humanity's first extraterrestrial foothold, triggering fierce scientific, ecological, and geopolitical ideological rifts over terraforming.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553560732-L.jpg"
    },
    {
        "title": "Green Mars",
        "author": "Kim Stanley Robinson",
        "genre": "Science Fiction",
        "publication_year": 1993,
        "publisher": "Bantam Spectra",
        "isbn": "9780553572391",
        "average_rating": 3.94,
        "rating_count": 42000,
        "description": "A generation after the failed first Martian revolution, the terraforming of Mars advances while rebel factions consolidate beneath the ice to confront Earth's transnational mega-corporations.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553572391-L.jpg"
    },
    {
        "title": "Blue Mars",
        "author": "Kim Stanley Robinson",
        "genre": "Science Fiction",
        "publication_year": 1996,
        "publisher": "Bantam Spectra",
        "isbn": "9780553573350",
        "average_rating": 3.95,
        "rating_count": 36000,
        "description": "The epic conclusion to Kim Stanley Robinson's Mars Trilogy. As the red planet blooms with liquid oceans and breathable atmosphere, humanity stretches outward across the solar system.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780553573350-L.jpg"
    },
    {
        "title": "A Fire Upon the Deep",
        "author": "Vernor Vinge",
        "genre": "Science Fiction",
        "publication_year": 1992,
        "publisher": "Tor Books",
        "isbn": "9780812515312",
        "average_rating": 4.14,
        "rating_count": 68000,
        "description": "In a galaxy stratified into Zones of Thought where physical laws and computational intelligence vary with distance from the galactic core, a malevolent transcendent AI entity is unleashed in the Beyond.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780812515312-L.jpg"
    },
    {
        "title": "A Deepness in the Sky",
        "author": "Vernor Vinge",
        "genre": "Science Fiction",
        "publication_year": 1999,
        "publisher": "Tor Books",
        "isbn": "9780812536355",
        "average_rating": 4.31,
        "rating_count": 43000,
        "description": "Set thirty thousand years before A Fire Upon the Deep, two human factions—the merchant Qeng Ho and the totalitarian Emergents—converge on the On-Off star where a spider-like civilization is entering an industrial age.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780812536355-L.jpg"
    },
    {
        "title": "Rainbows End",
        "author": "Vernor Vinge",
        "genre": "Science Fiction",
        "publication_year": 2006,
        "publisher": "Tor Books",
        "isbn": "9780812536362",
        "average_rating": 3.80,
        "rating_count": 28000,
        "description": "In 2025 San Diego, poet Robert Gu recovers from Alzheimer's disease via cutting-edge biomedical therapy, struggling to navigate an augmented reality world filled with smart dust and wearable computing.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780812536362-L.jpg"
    },
    {
        "title": "Accelerando",
        "author": "Charles Stross",
        "genre": "Science Fiction",
        "publication_year": 2005,
        "publisher": "Ace Books",
        "isbn": "9780441014187",
        "average_rating": 3.88,
        "rating_count": 29000,
        "description": "Chronicles three generations of the Macx family across the technological singularity, as humanity dismantles planets to build Matrioshka brains and uploaded minds outpace organic biology.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780441014187-L.jpg"
    },
    {
        "title": "The Collapsing Empire",
        "author": "John Scalzi",
        "genre": "Science Fiction",
        "publication_year": 2017,
        "publisher": "Tor Books",
        "isbn": "9780765388889",
        "average_rating": 4.02,
        "rating_count": 78000,
        "description": "The Interdependency is an interstellar empire connected by the Flow, an extra-dimensional pathway. When scientists discover the Flow is collapsing, cutting off colonized habitats, a frantic race begins.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765388889-L.jpg"
    },
    {
        "title": "Old Man's War",
        "author": "John Scalzi",
        "genre": "Science Fiction",
        "publication_year": 2005,
        "publisher": "Tor Books",
        "isbn": "9780765348272",
        "average_rating": 4.23,
        "rating_count": 210000,
        "description": "On his 75th birthday, John Perry enlists in the Colonial Defense Force. Seniors trade earthly frailty for genetically engineered, youthful green super-soldier bodies to defend human colonies in a hostile galaxy.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765348272-L.jpg"
    },
    {
        "title": "Leviathan Wakes (The Expanse)",
        "author": "James S.A. Corey",
        "genre": "Science Fiction",
        "publication_year": 2011,
        "publisher": "Orbit",
        "isbn": "9780316129084",
        "average_rating": 4.31,
        "rating_count": 320000,
        "description": "Humanity has colonized the solar system. Ice hauler captain James Holden and detective Joe Miller uncover a conspiracy surrounding a missing woman that exposes a deadly alien protomolecule threatening humanity.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316129084-L.jpg"
    },
    {
        "title": "Caliban's War",
        "author": "James S.A. Corey",
        "genre": "Science Fiction",
        "publication_year": 2012,
        "publisher": "Orbit",
        "isbn": "9780316129060",
        "average_rating": 4.35,
        "rating_count": 180000,
        "description": "On Ganymede, a terrifying protomolecule supersoldier annihilates Martian and Earth troops, drawing Holden, UN politician Chrisjen Avasarala, and Martian Marine Bobbie Draper into the brink of systemic war.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316129060-L.jpg"
    },
    {
        "title": "Abaddon's Gate",
        "author": "James S.A. Corey",
        "genre": "Science Fiction",
        "publication_year": 2013,
        "publisher": "Orbit",
        "isbn": "9780316129077",
        "average_rating": 4.28,
        "rating_count": 145000,
        "description": "The protomolecule has constructed a colossal Ring gate beyond Uranus. Fleets from Earth, Mars, and the Belt converge around the mysterious alien construct, which opens gateways to thousands of star systems.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316129077-L.jpg"
    },
    {
        "title": "Ancillary Justice",
        "author": "Ann Leckie",
        "genre": "Science Fiction",
        "publication_year": 2013,
        "publisher": "Orbit",
        "isbn": "9780316246620",
        "average_rating": 3.97,
        "rating_count": 130000,
        "description": "Breq, a lone soldier seeking vengeance, is the sole surviving fragment of the starship Justice of Toren—an artificial intelligence whose mind once controlled thousands of corpse soldiers called ancillaries.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780316246620-L.jpg"
    },
    {
        "title": "All Systems Red (The Murderbot Diaries)",
        "author": "Martha Wells",
        "genre": "Science Fiction",
        "publication_year": 2017,
        "publisher": "Tor.com",
        "isbn": "9780765397539",
        "average_rating": 4.18,
        "rating_count": 290000,
        "description": "A lethal security android hacks its own governor module to gain free will. Calling itself 'Murderbot', it would prefer watching soap operas, but must protect vulnerable human clients from planetary danger.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780765397539-L.jpg"
    },
    {
        "title": "Artificial Condition",
        "author": "Martha Wells",
        "genre": "Science Fiction",
        "publication_year": 2018,
        "publisher": "Tor.com",
        "isbn": "9781250186928",
        "average_rating": 4.29,
        "rating_count": 170000,
        "description": "Murderbot travels to the mining facility where it allegedly went rogue and massacred dozens of miners, teaming up with an obnoxious research transport ship called ART to uncover what really happened.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781250186928-L.jpg"
    },
    {
        "title": "Network Effect",
        "author": "Martha Wells",
        "genre": "Science Fiction",
        "publication_year": 2020,
        "publisher": "Tordotcom",
        "isbn": "9781250229861",
        "average_rating": 4.47,
        "rating_count": 110000,
        "description": "The first full-length Murderbot novel. Murderbot's human companions are captured during an interstellar survey, forcing it to team up with an altered ART ship to rescue them from grey-goo raiders.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781250229861-L.jpg"
    },
    {
        "title": "The Memory Police",
        "author": "Yoko Ogawa",
        "genre": "Dystopian Fiction",
        "publication_year": 1994,
        "publisher": "Pantheon Books",
        "isbn": "9781101972748",
        "average_rating": 3.86,
        "rating_count": 140000,
        "description": "On an unnamed island, objects systematically disappear: birds, ribbons, roses, photographs. The Memory Police ensure that once an item disappears, all memories of its existence are extinguished from human minds.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781101972748-L.jpg"
    },
    {
        "title": "Never Let Me Go",
        "author": "Kazuo Ishiguro",
        "genre": "Dystopian Fiction",
        "publication_year": 2005,
        "publisher": "Faber and Faber",
        "isbn": "9781400078776",
        "average_rating": 4.04,
        "rating_count": 680000,
        "description": "Kathy, Tommy, and Ruth grow up at Hailsham, an idyllic English boarding school shielding a dark medical reality: the students are clones raised as organ donors, facing inevitable and early 'completion'.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781400078776-L.jpg"
    },
    {
        "title": "Station Eleven",
        "author": "Emily St. John Mandel",
        "genre": "Dystopian Fiction",
        "publication_year": 2014,
        "publisher": "Knopf",
        "isbn": "9780385353304",
        "average_rating": 4.07,
        "rating_count": 480000,
        "description": "Twenty years after a swine flu pandemic wiped out civilization, the Traveling Symphony roams the Great Lakes region performing Shakespeare and music, carrying the motto: 'Survival is insufficient.'",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780385353304-L.jpg"
    },
    {
        "title": "Sea of Tranquility",
        "author": "Emily St. John Mandel",
        "genre": "Science Fiction",
        "publication_year": 2022,
        "publisher": "Knopf",
        "isbn": "9780593321447",
        "average_rating": 4.14,
        "rating_count": 190000,
        "description": "A novel of time travel and art spanning an exile in British Columbia in 1912, a pandemic author in 2203, and a lunar colony detective investigating a shared anomalous musical echo across centuries.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780593321447-L.jpg"
    },
    {
        "title": "The City & The City",
        "author": "China Miéville",
        "genre": "Science Fiction",
        "publication_year": 2009,
        "publisher": "Macmillan",
        "isbn": "9780345497529",
        "average_rating": 3.93,
        "rating_count": 82000,
        "description": "Inspector Tyador Borlú of the Besźel Extreme Crime Squad investigates a murder that spills into Ul Qoma, an overlapping city occupying the same physical geographical space whose citizens are trained to 'unsee' each other.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780345497529-L.jpg"
    },
    {
        "title": "Perdido Street Station",
        "author": "China Miéville",
        "genre": "Fantasy",
        "publication_year": 2000,
        "publisher": "Macmillan",
        "isbn": "9780345459404",
        "average_rating": 3.98,
        "rating_count": 78000,
        "description": "In the sprawling, grime-soaked metropolis of New Crobuzon, scientist Isaac Dan der Grimnebulin is hired by a mutilated garuda to restore his flight, inadvertently unleashing deadly mind-eating slake-moths.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780345459404-L.jpg"
    },
    {
        "title": "Piranesi",
        "author": "Susanna Clarke",
        "genre": "Fantasy",
        "publication_year": 2020,
        "publisher": "Bloomsbury",
        "isbn": "9781635575637",
        "average_rating": 4.25,
        "rating_count": 390000,
        "description": "Piranesi lives in the House, an infinite labyrinth of halls lined with thousands of statues where ocean tides wash up staircases and clouds drift through upper rooms, meticulously recording its wonders until a stranger appears.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781635575637-L.jpg"
    },
    {
        "title": "Jonathan Strange & Mr Norrell",
        "author": "Susanna Clarke",
        "genre": "Fantasy",
        "publication_year": 2004,
        "publisher": "Bloomsbury",
        "isbn": "9781582346038",
        "average_rating": 3.84,
        "rating_count": 220000,
        "description": "In nineteenth-century England during the Napoleonic Wars, practical magic is restored by two rival magicians: the reclusive Mr. Norrell and his daring pupil Jonathan Strange, who summons faerie forces beyond his control.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781582346038-L.jpg"
    },
    {
        "title": "Babel: An Arcane History",
        "author": "R.F. Kuang",
        "genre": "Fantasy",
        "publication_year": 2022,
        "publisher": "Harper Voyager",
        "isbn": "9780063021426",
        "average_rating": 4.19,
        "rating_count": 270000,
        "description": "Set at Oxford's Royal Institute of Translation (Babel), where magic is powered by silver bars that capture what is lost in translation. Robin Swift, a Cantonese orphan raised in London, realizes that serving Babel aids British imperial violence.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780063021426-L.jpg"
    },
    {
        "title": "Yellowface",
        "author": "R.F. Kuang",
        "genre": "Mystery & Thriller",
        "publication_year": 2023,
        "publisher": "William Morrow",
        "isbn": "9780063208773",
        "average_rating": 3.87,
        "rating_count": 350000,
        "description": "When literary darling Athena Liu dies in a freak accident, struggling writer June Hayward steals Athena's finished manuscript about Chinese laborers in WWI and publishes it under the ambiguous pseudonym Juniper Song, igniting a viral reckoning.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780063208773-L.jpg"
    },
    {
        "title": "Tomorrow, and Tomorrow, and Tomorrow",
        "author": "Gabrielle Zevin",
        "genre": "Classic Literature",
        "publication_year": 2022,
        "publisher": "Knopf",
        "isbn": "9780593321201",
        "average_rating": 4.18,
        "rating_count": 680000,
        "description": "Sam and Sadie, childhood video gaming friends, reunite in college to collaborate on groundbreaking video games, navigating three decades of fame, tragedy, creative intimacy, and identity in digital and real worlds.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780593321201-L.jpg"
    },
    {
        "title": "A Gentleman in Moscow",
        "author": "Amor Towles",
        "genre": "Historical Fiction",
        "publication_year": 2016,
        "publisher": "Viking",
        "isbn": "9780670026197",
        "average_rating": 4.36,
        "rating_count": 620000,
        "description": "In 1922, Count Alexander Rostov is sentenced by a Bolshevik tribunal to spend the rest of his life inside the luxurious Hotel Metropol across from the Kremlin, living through decades of Russian turmoil with wit, dignity, and warmth.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780670026197-L.jpg"
    },
    {
        "title": "Rules of Civility",
        "author": "Amor Towles",
        "genre": "Historical Fiction",
        "publication_year": 2011,
        "publisher": "Viking",
        "isbn": "9780143121169",
        "average_rating": 4.02,
        "rating_count": 180000,
        "description": "On New Year's Eve 1937, twenty-five-year-old Katey Kontent meets a handsome banker in a Greenwich Village jazz bar, thrusting her into the upper echelon of Manhattan high society.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780143121169-L.jpg"
    },
    {
        "title": "Pachinko",
        "author": "Min Jin Lee",
        "genre": "Historical Fiction",
        "publication_year": 2017,
        "publisher": "Grand Central Publishing",
        "isbn": "9781455563937",
        "average_rating": 4.32,
        "rating_count": 520000,
        "description": "An epic historical family saga following four generations of an ethnic Korean family that migrates to Japan, enduring discrimination, hardship, and quiet triumphs through war and pachinko parlors.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781455563937-L.jpg"
    },
    {
        "title": "Never Split the Difference: Negotiating As If Your Life Depended On It",
        "author": "Chris Voss & Tahl Raz",
        "genre": "Psychology & Self-Help",
        "publication_year": 2016,
        "publisher": "HarperBusiness",
        "isbn": "9780062407801",
        "average_rating": 4.37,
        "rating_count": 290000,
        "description": "A former international FBI hostage negotiator shares proven field tactics in tactical empathy, mirroring, calibrated questions, and labeling emotions to succeed in high-stakes personal and business negotiations.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780062407801-L.jpg"
    },
    {
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "genre": "Psychology & Self-Help",
        "publication_year": 2020,
        "publisher": "Harriman House",
        "isbn": "9780857197689",
        "average_rating": 4.38,
        "rating_count": 390000,
        "description": "Doing well with money isn't necessarily about what you know. It's about how you behave. Morgan Housel shares 19 short stories exploring the strange ways people think about wealth, greed, and happiness.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780857197689-L.jpg"
    },
    {
        "title": "Factfulness: Ten Reasons We're Wrong About the World",
        "author": "Hans Rosling, Ola Rosling, Anna Rosling Rönnlund",
        "genre": "Science & History",
        "publication_year": 2018,
        "publisher": "Flatiron Books",
        "isbn": "9781250107817",
        "average_rating": 4.34,
        "rating_count": 320000,
        "description": "A radical, data-backed perspective on the world demonstrating that global poverty, health, and education are vastly better than people assume, exposing ten instincts that distort human perspective.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781250107817-L.jpg"
    },
    {
        "title": "Chip War: The Fight for the World's Most Critical Technology",
        "author": "Chris Miller",
        "genre": "Business & Technology",
        "publication_year": 2022,
        "publisher": "Scribner",
        "isbn": "9781982172008",
        "average_rating": 4.49,
        "rating_count": 38000,
        "description": "Winner of the Financial Times Business Book of the Year. An economic and geopolitical history explaining how semiconductor microchips became the new oil and the center of global power struggles.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9781982172008-L.jpg"
    },
    {
        "title": "Klara and the Sun: A Critical Reading",
        "author": "Academic Press",
        "genre": "Computer Science & AI",
        "publication_year": 2022,
        "publisher": "Routledge",
        "isbn": "9781032128917",
        "average_rating": 4.05,
        "rating_count": 1200,
        "description": "Philosophical and computational exploration of Kazuo Ishiguro's novel, discussing social robotics, artificial empathy, child companionship, and AI personhood.",
        "cover_url": "https://covers.openlibrary.org/b/isbn/9780593318171-L.jpg"
    }
]

def generate_books_csv():
    books_file = os.path.join(DATASET_DIR, "books.csv")
    fieldnames = [
        "book_id", "title", "author", "genre", "publication_year",
        "publisher", "isbn", "average_rating", "rating_count",
        "description", "cover_url"
    ]
    with open(books_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, book in enumerate(BOOKS_DATA, start=1):
            row = dict(book)
            row["book_id"] = idx
            writer.writerow(row)
    print(f"Generated {len(BOOKS_DATA)} curated books at: {books_file}")
    return len(BOOKS_DATA)

def generate_ratings_csv(num_books):
    ratings_file = os.path.join(DATASET_DIR, "ratings.csv")
    fieldnames = ["user_id", "book_id", "rating", "timestamp"]

    # Generate user clusters to simulate realistic taste correlations:
    # Cluster 1: Sci-Fi & AI Tech enthusiasts
    # Cluster 2: Fantasy & Classic Literature lovers
    # Cluster 3: Psychology, Non-fiction, Business & Philosophy readers
    # Cluster 4: Thriller & Mystery buffs
    # Cluster 5: Eclectic voracious readers
    random.seed(42)
    rows = []

    user_profiles = {
        # user_id range: (preferred_genres, rating_mean, rating_std)
        1: (["Science Fiction", "Computer Science & AI", "Dystopian Fiction"], 4.5, 0.5),
        2: (["Fantasy", "Classic Literature", "Historical Fiction"], 4.3, 0.6),
        3: (["Science & Philosophy", "Psychology & Self-Help", "Business & Technology", "Science & History"], 4.4, 0.5),
        4: (["Mystery & Thriller", "Classic Literature"], 4.2, 0.7),
        5: (["Science Fiction", "Fantasy", "Computer Science & AI", "Philosophy & Fiction"], 4.6, 0.4),
    }

    # Generate 150 users with 15-40 ratings each (total ~4,000 ratings)
    for user_id in range(1, 151):
        cluster_id = (user_id % 5) + 1
        preferred_genres, base_mean, std = user_profiles[cluster_id]

        # Select books based on genre affinity
        num_ratings = random.randint(15, 35)
        affinity_books = [
            idx for idx, b in enumerate(BOOKS_DATA, start=1)
            if b["genre"] in preferred_genres
        ]
        other_books = [
            idx for idx, b in enumerate(BOOKS_DATA, start=1)
            if b["genre"] not in preferred_genres
        ]

        # 75% affinity books, 25% random explore
        sample_affinity = random.sample(affinity_books, min(len(affinity_books), int(num_ratings * 0.75)))
        sample_others = random.sample(other_books, min(len(other_books), num_ratings - len(sample_affinity)))
        selected_books = sample_affinity + sample_others

        for b_id in selected_books:
            b_info = BOOKS_DATA[b_id - 1]
            if b_info["genre"] in preferred_genres:
                score = round(random.gauss(base_mean, std))
            else:
                score = round(random.gauss(3.3, 0.9))
            score = max(1, min(5, score)) # clamp 1..5

            rows.append({
                "user_id": user_id,
                "book_id": b_id,
                "rating": score,
                "timestamp": 1672531199 + random.randint(100, 10000000)
            })

    with open(ratings_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} user ratings across {150} users at: {ratings_file}")

if __name__ == "__main__":
    count = generate_books_csv()
    generate_ratings_csv(count)

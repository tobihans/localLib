from django.db import models
import uuid  # Required for unique book instances
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


# Author
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"""
        {{
            'id': {self.id},
            'first_name': {self.first_name},
            'last_name': {self.last_name},
            'date_of_birth': {self.date_of_birth},
            'date_of_death': {self.date_of_death},
            '#created_at': {self.created_at},
            '#updated_at': {self.updated_at}
        }}
        """


# Genre
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Genre du livre. E.g. Roman, Aventure")
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"""
        {{
            'id': {self.id},
            'name': {self.name},
            '#created_at': {self.created_at},
            '#updated_at': {self.updated_at}
        }}
        """


class Language(models.Model):
    language = models.CharField(max_length=100)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"""
        {{
            'id': {self.id},
            'language': {self.language},
            '#created_at': {self.created_at},
            '#updated_at': {self.updated_at}
        }}
        """


# Book
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    original_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String for representing the Model object."""
        return f"""
        {{
            'id': {self.id},
            'title': {self.title},
            'author': #{self.author.id},
            'original_language': #{self.original_language},
            'summary': {self.summary},
            'isbn': %{self.isbn}%
            'genre': #[
                {self.genre}
            ],
            '#created_at': {self.created_at},
            '#updated_at': {self.updated_at}
        }}
        """

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def original_lang(self):
        return self.original_language.language

    original_lang.short_description = 'Language'

    def author_name(self):
        return f"{self.author.last_name} {self.author.first_name}"


# BooInstance
class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f"""
        {{
            'id': {self.id},
            'book': #{self.book.id},
            'language': #{self.language}
            'imprint': {self.imprint},
            'due_back': {self.due_back},
            'status': {self.status},
            '#created_at': {self.created_at},
            '#updated_at': {self.updated_at}
        }}
        """

    def book_title(self):
        return self.book.title

    book_title.short_description = 'Book'

    def lang(self):
        # This is like that because of a bug I encountered recently
        # concerning language as it' snot required in the form,
        # and i forgot filling it
        return self.language.language if self.language is not None else ''

    lang.short_description = 'Language'


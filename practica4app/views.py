from .models import Book, Library
from .models import Book, Library
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book, Library, Loan, User

# library-----------------------------------------------------------------------------------------------


def list_libraries(request):
    try:
        libraries = list(Library.objects.values("id", "name"))
        return JsonResponse(libraries, safe=False)
    except Library.DoesNotExist:
        return JsonResponse({"error": "No hay ninguna biblioteca registrada"}, status=404)
    else:
        return JsonResponse({'error': 'Método HTTP no permitido, use POST'}, status=405)


@csrf_exempt
def new_library(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            newLibrary = Library.objects.create(
                name=data['name']
            )
            return JsonResponse({"mensaje": "Biblioteca registrada con éxito", "libraryId": newLibrary.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


def get1_library(request, library_id):
    try:
        library = Library.objects.values("id", "name").get(id=library_id)
        return JsonResponse(library)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Biblioteca no encontrada"}, status=404)

# books-----------------------------------------------------------------------------------------------


def list_all_books(request):
    try:
        books = list(Book.objects.values("id", "title", "author", "library"))
        return JsonResponse(books, safe=False)
    except Book.DoesNotExist:
        return JsonResponse({"error": "No hay ningun libro registrado"}, status=404)


@csrf_exempt
def new_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            library = Library.objects.get(id=data['library_id'])
            newBook = Book.objects.create(
                title=data['title'],
                author=data['author'],
                library=library
            )
            return JsonResponse({"mensaje": "Libro registrado con éxito", "book_id": newBook.id})

        except Library.DoesNotExist:
            return JsonResponse({"error": "Librería no encontrada"}, status=404)

        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def books_by_library(request, library_id):
    try:
        books = list(Book.objects.filter(library_id=library_id).values(
            "id", "title", "author", "library"))
        return JsonResponse(books, safe=False)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Libro no encontrado"}, status=404)


def get1_book(request, book_id):
    try:
        book = Book.objects.values(
            "id", "title", "author", "library").get(id=book_id)
        return JsonResponse(book)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Libro no encontrado"}, status=404)


@csrf_exempt
def update_book(request, book_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book = Book.objects.get(id=book_id)
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            library_id = data.get('library')
            if library_id is not None:
                try:
                    library = Library.objects.get(id=library_id)
                    book.library = library
                except Library.DoesNotExist:
                    return JsonResponse({'error': 'La biblioteca que quiere asignarle al libro no existe'}, status=404)
            book.save()
            return JsonResponse({'message': 'Libro actualizado con éxito', 'libro': {'title': book.title, 'author': book.author, 'library': book.library.name}}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Libro que se quiere actualizar no fue encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete_book(request, book_id):
    if request.method == 'POST':
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return JsonResponse({'message': 'Libro eliminado con éxito'}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Libro no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Método HTTP no permitido, use POST'}, status=405)

# users-----------------------------------------------------------------------------------------------


def list_users(request):
    try:
        users = list(User.objects.values("id", "name"))
        return JsonResponse(users, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error": "No hay ningun usuario registrado"}, status=404)


@csrf_exempt
def new_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            newUser = User.objects.create(
                name=data['name']
            )
            return JsonResponse({"mensaje": "Usuario registrada con éxito", "userId": newUser.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


def get1_user(request, user_id):
    try:
        user = User.objects.values(
            "id", "name").get(id=user_id)
        return JsonResponse(user)
    except User.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


# loans-------------------------------------------------------------------------------------------
@csrf_exempt
def new_loan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_ = Book.objects.get(id=data['book_id'])
            user_ = User.objects.get(id=data['user_id'])
            newLoan = Loan.objects.create(
                book=book_,
                user=user_,
                date_start=timezone.now(),
                date_end=None
            )
            return JsonResponse({"mensaje": "Prestamo registrado con éxito", "loan_id": newLoan.id})

        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no encontrado"}, status=404)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


def list_loans(request):
    try:
        loans = list(Loan.objects.values(
            "id", "book", "user", "date_start", "date_end"))
        return JsonResponse(loans, safe=False)
    except Loan.DoesNotExist:
        return JsonResponse({"error": "No hay ningun prestamo registrado"}, status=404)


@csrf_exempt
def loans_by_user(request, user_id):
    try:
        loans = list(Loan.objects.filter(user_id=user_id).values(
            "id", "book", "user", "date_start", "date_end"))
        return JsonResponse(loans, safe=False)
    except Loan.DoesNotExist:
        return JsonResponse({"error": "Prestamo no encontrado"}, status=404)


@csrf_exempt
def return_book(request, loan_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            loan = Loan.objects.get(id=loan_id)
            loan.date_end = timezone.now()
            loan.save()
            return JsonResponse({'message': 'Libro devuelto con éxito'}, status=200)
        except Loan.DoesNotExist:
            return JsonResponse({'error': 'Prestamo  no fue encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

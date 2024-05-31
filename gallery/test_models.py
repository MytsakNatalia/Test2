from django.test import TestCase
from gallery.models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class CategoryCreationTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Animals")
        self.assertEqual(str(category), category.name)
        self.assertEqual(category.name, "Animals")

class ImageCreationTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Nature")
        self.image_file = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02', content_type='image/jpeg')
        self.image = Image.objects.create(
            title="Sunset",
            image=self.image_file,
            created_date=datetime.date.today(),
            age_limit=18
        )
        self.image.categories.add(self.category)

    def test_create_image(self):
        self.assertEqual(str(self.image), self.image.title)
        self.assertEqual(self.image.title, "Sunset")
        self.assertEqual(self.image.age_limit, 18)
        self.assertIn(self.category, self.image.categories.all())

    def test_image_category_relation(self):
        image = Image.objects.get(title="Sunset")
        self.assertEqual(image.categories.count(), 1)
        self.assertEqual(image.categories.first(), self.category)


class CategoryDeletionTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name="Nature")
        self.category2 = Category.objects.create(name="Mountains")
        self.image_file = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02', content_type='image/jpeg')
        self.image = Image.objects.create(
            title="Sunset",
            image=self.image_file,
            created_date=datetime.date.today(),
            age_limit=18
        )
        self.image.categories.add(self.category1)
        self.image.categories.add(self.category2)

    def test_category_deletion(self):
        # Before deletion
        self.assertEqual(self.image.categories.count(), 2)

        # Delete one category
        self.category1.delete()

        # After deletion
        self.image.refresh_from_db()
        self.assertEqual(self.image.categories.count(), 1)
        self.assertEqual(self.image.categories.first(), self.category2)

    def test_image_category_cleanup(self):
        # Ensure both categories are linked
        self.assertEqual(self.image.categories.count(), 2)

        # Delete all categories
        self.category1.delete()
        self.category2.delete()

        # Refresh the image instance from the database
        self.image.refresh_from_db()
        self.assertEqual(self.image.categories.count(), 0)

    def test_cascade_delete(self):
        # Ensure the Image instance exists
        self.assertEqual(Image.objects.count(), 1)

        # Delete a category and check if Image instance is still there
        self.category1.delete()
        self.assertEqual(Image.objects.count(), 1)

        # Delete the remaining category
        self.category2.delete()
        self.assertEqual(Image.objects.count(), 1)
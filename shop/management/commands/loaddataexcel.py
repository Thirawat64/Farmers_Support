# your_app/management/commands/loaddataexcel.py
from django.core.management.base import BaseCommand
from shop.models import Provinces
import pandas as pd

class Command(BaseCommand):
    help = 'Load data from Excel file into database'

    def handle(self, *args, **kwargs):
        excel_file = 'Provinces.xlsx'  # เปลี่ยนเป็นเส้นทางไปยังไฟล์ Excel ของคุณ
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            product = Provinces(
                province_name=row[0],

                # เพิ่มฟิลด์อื่น ๆ ตามต้องการ
            )
            product.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))

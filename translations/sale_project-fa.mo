��    @        Y         �  �  �                    "  	   4     >     N     S     a     s     �     �  ;   �  +   �                    '  	   4  1  >     p	  
   �	     �	  6  �	     �
     �
                    %     6     K  "   T     w     �     �     �     �     �     �     �     �  +   �  (   (  <   Q     �     �     �     �     �     �     �  Q   �  c   F  d   �       
              .     >     P  n   ]    �  x  �     \     r  
   �     �     �     �     �     �          !     =     M  l   i  L   �     #     7  !   H     j     �  
  �  7   �     �     �  �    +        .  
   K     V  
   j     u     �     �  J   �  
     %        6     U     ^     r  %   �     �     �  @   �  @   +  �   l  '   �       
   *     5  
   K     V  *   l  x   �  ~     �   �     &     8     N      f  *   �  +   �  �   �            4          #       7   >       '          (   9             :              
                   ;       5       <          8   @   =       !      ?   3       "             %         $   *       6              /   -         .   	          ,      2   &      +                 0                        1              )    According to product configuration, the delivered quantity can be automatically computed by mechanism:
  - Manual: the quantity is set manually on the line
  - Analytic From expenses: the quantity is the quantity sum from posted expenses
  - Timesheet: the quantity is the sum of hours recorded on tasks linked to this sale line
  - Stock Moves: the quantity comes from confirmed pickings
 Billable Canceled Customer Customer Invoices Delivered Display project Done Down Payments Generated Project Generated Task In Progress Invoice Count Invoice ordered quantities as soon as this service is sold. Invoice your time and material to customers Invoiced Invoices Invoicing Policy Journal Item Load more Manually set quantities on order: Invoice based on the manually entered quantity, without creating an analytic account.
Timesheets on contract: Invoice based on the tracked hours on the related timesheet.
Create a task and track hours: Create a task on the sales order validation and track the work hours. Method to update delivered qty Milestones Non-billable On Sales order confirmation, this product can generate a project and/or task.         From those, you can track the service you are selling.
         'In sale order's project': Will use the sale order's configured project if defined or fallback to         creating a new project based on the selected template. Operation not supported Other Services Product Product Variant Project Project Template Project's sale order Projects Projects used in this sales order. Quantity Quotation Template Line Sale Order Count Sales Sales Order Sales Order Item Sales Order Items Sales Order Line Sales Orders Sales order to which the project is linked. Sales order to which the task is linked. Select a non billable project on which tasks can be created. Service Invoicing Policy Sold Task Task Recurrence Tasks Tasks Analysis Tasks associated to this sale The product %s should not have a global project since it will generate a project. The product %s should not have a project nor a project template since it will not generate project. The product %s should not have a project template since it will generate a task in a global project. To Do To invoice Track Service Unit of Measure Vendor Bill Count Vendor Bills You cannot link the order item %(order_id)s - %(product_id)s to this task because it is a re-invoiced expense. Project-Id-Version: Odoo Server 17.0
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2024-09-14 09:41+0330
Last-Translator: 
Language-Team: 
Language: fa
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: 
X-Generator: Poedit 3.2.2
 باتوجه به پیکربندی محصول، مقدار تحویل شده می‌تواند به طور خودکار با مکانیزم محاسبه شود:
 - دستی: کمیت به صورت دستی روی خط تنظیم می‌شود
 - تحلیلی از هزینه‌ها: کمیت مجموع مقدار از هزینه‌های ثبت شده است
 - برگه کارکرد: مقدار عبارت است از مجموع ساعات ضبط شده بر روی وظایف مربوط به این سطر فروش است
 - انتقال موجودی: کمیت از برداشت‌های تاییدشده بدست می‌آید.
 قابل فاکتور لغو شده مشتری فاکتورهای مشتری تحویل داده شد نمایش پروژه انجام شده پیش پرداخت‌ها پروژه ایجادشده وظایف ایجادشده در جریان تعداد فاکتورها به محض فروش این سرویس، مقادیر سفارش داده شده را فاکتور کنید. زمان و اجناس خود را برای مشتری فاکتور کنید فاکتور شده فاکتورها خط مشی صدور فاکتور آیتم دفترروزنامه بارگذاری بیشتر تنظیم دستی مقادیر بر اساس سفارش: فاکتور بر اساس مقدار شده به صورت دستی، بدون ایجاد یک حساب تحلیلی. 
برگه‌های ساعت کارکرد در قرارداد: فاکتور بر اساس ساعات ردیابی شده بر روی برگه ساعت کارکرد زمانی مربوطه. 
ایجاد یک وظیفه و ردیابی ساعت: ایجاد یک وظیفه در ارزشیابی سفارش فروش و پیگیری ساعات کار. روش بروز رسانی تعداد تحویل شده موعد ها غیرقابل پرداخت در تایید سفارش فروش، این محصول می‌تواند یک پروژه و / یا وظیفه تولید کند. از آن‌ها، شما می‌توانید خدماتی را که می‌فروشید را دنبال کنید.
در پروژه سفارش فروش: در صورت تعریف و یا پشتیبان برای ایجاد یک پروژه جدید براساس الگوی انتخاب‌شده از پروژه پیکربندی شده فروش استفاده کنید. عملیات پشتیبانی نمی شود سرویس‌های دیگر محصول گونه محصول پروژه قالب پروژه سفارش فروش پروژه پروژه‌ها پروژه های مورد استفاده در این سفارش فروش. تعداد سطر قالب پیش‌فاکتور تعداد سفارش فروش فروش سفارش فروش آیتم سفارش فروش آیتم‌های سفارش فروش سطر سفارش‌فروش سفارشات فروش سفارش فروش که پروژه به آن مرتبط است. سفارش فروش که وظیفه به آن مرتبط است. یک پروژه غیرقابل پرداخت را انتخاب کنید که در آن می توان وظایف ایجاد کرد. خط مشی صورتحساب خدمات فروخته شده وظیفه تکرار وظیفه وظایف تحلیل کارها وظایف مرتبط با این فروش محصول %s نباید یک پروژه عمومی داشته باشد زیرا یک پروژه ایجاد می کند. محصول %s نباید پروژه یا قالب پروژه داشته باشد زیرا پروژه تولید نمی کند. محصول %s نباید قالب پروژه داشته باشد زیرا وظیفه ای را در یک پروژه عمومی ایجاد می کند. جهت اقدام برای فاکتور سرویس ردگیری واحد اندازه‌گیری تعداد صورتحساب فروشنده صورت‌حساب‌های فروشنده شما نمی توانید آیتم سفارش %(order_id)s - %(product_id)s را به این کار پیوند دهید زیرا هزینه ای است که مجدداً صورتحساب می شود. 
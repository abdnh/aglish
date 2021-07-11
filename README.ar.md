<div dir="rtl">

# Aglish

اقرأ بلغة: [English](README.md)

--------

إضافة [أنكي](https://apps.ankiweb.net/) لـ [YouGlish](https://youglish.com/)؛
خدمة تساعدك على تعلم لغة من خلال السياق بعرض فيديوهات يوتيوب تحتوي كلمة أو عبارة تريد تعلم نطقها أو معناها.

![YouGlish Widget](youglish-widget.png)

يدعم YouGlish عدة لغات وميزات للواجهة. تدعم هذه الإضافة كل اللغات المدعومة من قبل الإضافة
وبعض الميزات.

تدمج الإضافة YouGlish مع أنكي من خلال فلتر مخصص تضعه في قوالب بطاقاتك (`{{aglish:Front}}` مثلًا).

استخدامها سهل جدًا. لنأخذ بعض الأمثلة:

- `{{aglish lang=english accent=uk:Front}}`  
  يعرض هذا فيديوهات للنص الموجود في الحقل الأمامي بالإنجليزية البريطانية.
- واجهة الفيديو مخفية خلف زر بشكل افتراضي.
  تستطيع تغيير النص المعروض على الزر باستخدام خيار `label` (لا يسمح بالفراغات في النص الآن):  
  `{{aglish lang=english accent=uk label=youglish_english_uk:Front}}`
- يمكنك أيضًا جعل الفيديو يعمل تلقائيًا باستخدام خيار `autoplay`:  
  `{{aglish lang=english accent=uk autoplay:Front}}`  
  لكن انتبه إلى أنه إذا كنت تراجع بطاقات كثيرة مع تفعيل التشغيل التلقائي، فقد يتم حظرك
  من استخدام YouGlish مؤقتًا أو يطلب منك حل CAPTCHA. ينصح بتفعيل التشغيل التلقائي
  فقط عندما يكون الموضوع الرئيسي لنوع ملحوظاتك هو فيديوهات YouGlish، حيث لن تتخطى بطاقة
  قبل مشاهدة مقطع فيديو، وإلا ستكون تجاوب البطاقات بدون تفكير.
- تستطيع جمع فلتر أنكي `cloze-only` مع فلتر `aglish` للبحث عن عبارات ملء الفراغات فقط
  في أنواع ملحوظات الـcloze:  
  `{{aglish lang=english:cloze-only:Text}}`
- فلتر `cloze-only` يعمل في الجانب الخلفي فقط، لذلك توفر هذه الإضافة خيارًا مشابهًا (`clozeonly`)
  يعمل في كلا الجانبين:  
  `{{aglish lang=english clozeonly:Text}}`
- خيار `nocaps` مفيد هنا لإخفاء التعليقات التوضيحية أسفل الفيديو عندما تحوي الفيديوهات على كلمات
  محذوفة في الجانب الأمامي:  
  `{{aglish lang=english clozeonly nocaps:Text}}`
- تستطيع أيضًا تغيير سمة الواجهة باستخدام خيار `theme`:  
  `{{aglish theme=dark:Text}}`  
  الخيارات المتوفرة هي `light` و `dark` و `anki` (السمة المستخدمة في أنكي، الخيار الافتراضي).
- يمكن تغيير عرض الواجهة وارتفاعها باستخدام خياري `width` و `height`:  
  `{{aglish lang=arabic width=600 height=500:Front}}`  
  ستأخذ الواجهة حجم النافذة المحتوية إذا لم تخصص هذين الخيارين.

لكل الخيارات قيم افتراضية لذلك يمكنك إهمالها؛ `{{aglish:Front}}` يتفرض اللغة الإنجليزية بكل
لهجاتها، ويظهر واجهة بسمة أنكي مع التعليقات التوضيحية.

لرؤية كل اللغات واللهجات المدعومة، انظر [توثيق YouGlish](https://youglish.com/api/doc/js-api) (انزل للأسفل إلى توثيق دالة `widget.fetch`).

## مراجع

توثيق واجهة YouGlish
 - https://youglish.com/api/doc/widget
 - https://youglish.com/api/doc/js-api

</div>
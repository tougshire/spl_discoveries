from datetime import date
from django.db import models
from spl_members.models import Member as Staffmember


class Customer(models.Model):
    name_full = models.CharField(
        "name", max_length=80, help_text="The name of the customer"
    )
    name_prefered = models.CharField(
        "prefered name",
        max_length=30,
        blank=True,
        help_text="Nickname, or a name the customer prefers in place of their first name",
    )
    email = models.EmailField(
        "email", blank=True, help_text="The customer's email address"
    )
    phone = models.CharField(
        "phone", max_length=30, blank=True, help_text="The customer's phone number"
    )

    def __str__(self):
        return self.name_full

    class Meta:
        ordering = ("name_full",)


class Location(models.Model):
    name_full = models.CharField(
        "location name", max_length=40, help_text="The full name of the location"
    )
    name_abbr = models.CharField(
        "abbreviated name", max_length=5, help_text="An abbreviation of the name"
    )

    def __str__(self):
        return self.name_full

    class Meta:
        ordering = ("name_full",)


class Topic(models.Model):
    name = models.CharField("name", max_length=40, help_text="The name of the topic")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Inquiry(models.Model):

    name_full = models.CharField(
        "full name",
        max_length=120,
        help_text="Your full name",
    )
    name_prefered=models.CharField(
        "prefered name",
        max_length=30,
        blank=True,
        help_text="How you would like us to address you (ex: John, Jill, JT, Ms. Tiller )"
    )
    summary = models.CharField(
        "request summary",
        max_length=80,
        help_text="A summary of the assistance you're requesting",
    )
    details = models.TextField(
        "details",
        help_text="Optionally, more details about your request request",
    )
    availability = models.CharField(
        "availability",
        max_length=255,
        blank=True,
        help_text="Please describe what days or times would work best for you.  You can be specific (June 1ST or 2nd at 11:00) or more general (Monday afternoons or Wednesday evenings)",
    )
    where_desired = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The scheduled location for the appointment",
    )
    date_submitted = models.DateField(
        "date submitted",
        default=date.today,
        blank=True,
        null=True,
        help_text="The date that the customer submitted the request",
    )

    def __str__(self):
        return "{}: {}: {}".format(
            self.name_full, self.summary, self.date_submitted
        )

    class Meta:
        ordering = ("date_submitted",)


class Appointment(models.Model):

    title = models.CharField(
        "title",
        max_length=255,
        blank=True,
        help_text="A title for the appointment (ex, help Brenda with her tablet)",
    )
    customer = models.ForeignKey(
        Customer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The customer for  whom the apointment is made",
    )
    customers_availability = models.CharField(
        "customer's availability",
        max_length=255,
        blank=True,
        help_text="The customer's preference regarding scheduling",
    )
    request_summary = models.CharField(
        "request summary",
        blank=True,
        max_length=255,
        help_text="A summary of the customer's request",
    )
    date_submitted = models.DateField(
        "date submitted",
        blank=True,
        null=True,
        help_text="The date that the customer submitted the request",
    )
    staffer = models.ForeignKey(
        Staffmember,
        verbose_name="staff member",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The staff members who is assigned to this appontment or who did the appointment",
    )
    when_scheduled = models.DateTimeField(
        "when scheduled",
        blank=True,
        null=True,
        help_text="The date and time the appointment is scheduled",
    )
    where_scheduled = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The scheduled location for the appointment",
    )
    when_completed = models.DateTimeField(
        "when completed",
        blank=True,
        null=True,
        help_text="The date and time the appointment was done",
    )
    status = models.IntegerField(
        "status",
        choices=(
            (40, "Canceled"),
            (41, "No-Show"),
            (0, "Requested"),
            (10, "Contact Attempted"),
            (14, "Delayed"),
            (18, "Scheduled"),
            (99, "Complete"),
        ),
        help_text="The status of this appointment",
    )
    Inquiry = models.ForeignKey(
        Inquiry,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The inquiry upon which this appointment is based"
    )

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "{}: {}: {}".format(
                self.customer, self.when_scheduled, self.request_summary
            )

    class Meta:
        ordering = ('when_scheduled', 'date_submitted')


class Appointmentnote(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The appointment to which this note applies",
    )
    when = models.DateField(
        "when",
        null=True,
        default=date.today,
        help_text="The effective date of the information in the note ( rather than the date the note was made )",
    )
    content = models.CharField(
        "content",
        max_length=125,
        blank=True,
        help_text="The text of the note.  Optional if a category is chosen and no other details are necessary.",
    )

    def __str__(self):
        str = self.when.isoformat() + ": "
        if self.content:
            str = str + self.content + ": "
        if len(str) > 2:
            str = str[0:-2]
        if len(str) > 50:
            str = str[0:45] + " ..."

        return str

    class Meta:
        ordering = [
            "-when",
        ]


class Customernote(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The customer to whom this note applies",
    )
    when = models.DateField(
        "when",
        null=True,
        default=date.today,
        help_text="The effective date of the information in the note ( rather than the date the note was made )",
    )
    content = models.CharField(
        "description",
        max_length=125,
        blank=True,
        help_text="The text of the note.  Optional if a category is chosen and no other details are necessary.",
    )

    def __str__(self):
        str = self.when.isoformat() + ": "
        if self.content:
            str = str + self.content + ": "
        if len(str) > 2:
            str = str[0:-2]
        if len(str) > 50:
            str = str[0:45] + " ..."

        return str

    class Meta:
        ordering = [
            "-when",
        ]



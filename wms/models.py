# coding=utf-8

from django.db import models

class Provider(models.Model):
	name = models.CharField("供应商名",max_length=128, unique=True)
	desc = models.TextField("供应商描述", blank=True)
	contact = models.CharField("联系人", max_length=32, blank=True)
	tel1 = models.CharField("联系电话1", max_length=32, blank=True)
	tel2 = models.CharField("联系电话2", max_length=32, blank=True)
	mail = models.EmailField("电子邮件", blank=True)

	def __unicode__(self):
		return self.name

class Manufacturer(models.Model):
	name = models.CharField("制造商名",max_length=128, unique=True)
	desc = models.TextField("制造商描述", blank=True)

	def __unicode__(self):
		return self.name

class Project(models.Model):
	name = models.CharField("项目名",max_length=128, unique=True)
	desc = models.TextField("项目描述")
	owner = models.CharField("项目负责人",max_length=128)
	customer = models.CharField("项目客户",max_length=128)

	def __unicode__(self):
		return self.name

class ItemType(models.Model):
	name = models.CharField("物料类型名",max_length=128, unique=True)
	desc = models.TextField("类型描述", blank=True)

	def __unicode__(self):
		return self.name

class Item(models.Model):
	pn = models.CharField("物料编号", max_length=128, unique=True)
	opn = models.CharField("物料原厂编号", max_length=128)
	manufacturer = models.ForeignKey(Manufacturer, verbose_name="制造商")
	type = models.ForeignKey(ItemType, verbose_name="物料类型")
	value = models.CharField("型号/值", max_length=128)
	package = models.CharField("封装", max_length=64)
	desc = models.TextField("物料描述")
	num = models.IntegerField("库存数量", editable=False, default=0)

	def __unicode__(self):
		return self.pn

class Import(models.Model):
	item = models.ForeignKey(Item, verbose_name="物料")
	provider = models.ForeignKey(Provider, verbose_name="供应商")
	project = models.ForeignKey(Project, verbose_name="项目")
	num = models.PositiveIntegerField("购买数量")
	ver = models.CharField("购买版本号",max_length=128, blank=True)
	price = models.FloatField("单价")
	sum = models.FloatField("总价", editable=False)
	cycle = models.PositiveIntegerField("购买周期")
	min_num = models.PositiveIntegerField("最小采购量")
	min_price = models.FloatField("最小采购单价")
	desc = models.TextField("采购量和价格描述")
	pay_date = models.DateField("付款日期")
	arrive_date = models.DateField("应到货日期")
	arrived_date = models.DateField("实到货日期")
	enter_date = models.DateField("入库日期")

	def save(self, force_insert=False, force_update=False):
		delta = self.num
		if self.id is not None:
			selected_import = Import.objects.get(pk=self.pk)
			delta -= selected_import.num

		self.sum = self.price * self.num	
		super(Import, self).save(force_insert, force_update)

		if delta != 0:
				selected_item = Item.objects.get(pk=self.item.pk)
				selected_item.num += delta
				selected_item.save()

	def delete(self):		
		selected_import = Import.objects.get(pk=self.pk)
		delta = selected_import.num
		
		super(Import, self).delete()

		if delta != 0:
			selected_item = Item.objects.get(pk=self.item.pk)
			selected_item.num -= delta
			selected_item.save()

class Export(models.Model):
	item = models.ForeignKey(Item, verbose_name="物料")
	project = models.ForeignKey(Project, verbose_name="项目")
	issue_date = models.DateField("出库日期")
	num = models.PositiveIntegerField("出库数量")

	def save(self, force_insert=False, force_update=False):
		delta = self.num

		if self.id is not None:
			selected_export = Export.objects.get(pk=self.pk)
			delta -= selected_export.num

		super(Export, self).save(force_insert, force_update)
		
		if delta != 0:
			selected_item = Item.objects.get(pk=self.item.pk)
			selected_item.num -= delta
			selected_item.save()

	def delete(self):
		selected_export = Export.objects.get(pk=self.pk)
		delta = selected_export.num

		super(Export, self).delete()

		if delta != 0:
			selected_item = Item.objects.get(pk=self.item.pk)
			selected_item.num += delta
			selected_item.save()




import xlrd
import xlwt

from xlrd import open_workbook,cellnameabs
from xlutils.copy import copy
from xlwt import Style

def copyXF(rdbook,rdxf):
    """
    clone a XFstyle from xlrd XF class,the code is copied from xlutils.copy module
    """
    
    wtxf = xlwt.Style.XFStyle()
    #
    # number format
    #
    wtxf.num_format_str = rdbook.format_map[rdxf.format_key].format_str
    #
    # font
    #
    wtf = wtxf.font
    rdf = rdbook.font_list[rdxf.font_index]
    wtf.height = rdf.height
    wtf.italic = rdf.italic
    wtf.struck_out = rdf.struck_out
    wtf.outline = rdf.outline
    wtf.shadow = rdf.outline
    wtf.colour_index = rdf.colour_index
    wtf.bold = rdf.bold #### This attribute is redundant, should be driven by weight
    wtf._weight = rdf.weight #### Why "private"?
    wtf.escapement = rdf.escapement
    wtf.underline = rdf.underline_type #### 
    # wtf.???? = rdf.underline #### redundant attribute, set on the fly when writing
    wtf.family = rdf.family
    wtf.charset = rdf.character_set
    wtf.name = rdf.name
    # 
    # protection
    #
    wtp = wtxf.protection
    rdp = rdxf.protection
    wtp.cell_locked = rdp.cell_locked
    wtp.formula_hidden = rdp.formula_hidden
    #
    # border(s) (rename ????)
    #
    wtb = wtxf.borders
    rdb = rdxf.border
    wtb.left   = rdb.left_line_style
    wtb.right  = rdb.right_line_style
    wtb.top    = rdb.top_line_style
    wtb.bottom = rdb.bottom_line_style 
    wtb.diag   = rdb.diag_line_style
    wtb.left_colour   = rdb.left_colour_index 
    wtb.right_colour  = rdb.right_colour_index 
    wtb.top_colour    = rdb.top_colour_index
    wtb.bottom_colour = rdb.bottom_colour_index 
    wtb.diag_colour   = rdb.diag_colour_index 
    wtb.need_diag1 = rdb.diag_down
    wtb.need_diag2 = rdb.diag_up
    #
    # background / pattern (rename???)
    #
    wtpat = wtxf.pattern
    rdbg = rdxf.background
    wtpat.pattern = rdbg.fill_pattern
    wtpat.pattern_fore_colour = rdbg.pattern_colour_index
    wtpat.pattern_back_colour = rdbg.background_colour_index
    #
    # alignment
    #
    wta = wtxf.alignment
    rda = rdxf.alignment
    wta.horz = rda.hor_align
    wta.vert = rda.vert_align
    wta.dire = rda.text_direction
    # wta.orie # orientation doesn't occur in BIFF8! Superceded by rotation ("rota").
    wta.rota = rda.rotation
    wta.wrap = rda.text_wrapped
    wta.shri = rda.shrink_to_fit
    wta.inde = rda.indent_level
    # wta.merg = ????
    #
    return wtxf

wbOld = open_workbook("switch.xls",on_demand=True,formatting_info=True)
shOld = wbOld.sheet_by_index(0)

wbNew = xlwt.Workbook()
shNew = wbNew.add_sheet(shOld.name, cell_overwrite_ok=True)

for rownum in range(shOld.nrows):	
	rowOld = shOld.row_values(rownum)
	shNew.row(rownum).height = shOld.rowinfo_map[rownum].height
        shNew.row(rownum).hidden = shOld.rowinfo_map[rownum].hidden
	for colnum in range(shOld.ncols):
		wbxfOld = wbOld.xf_list[shOld.cell_xf_index(rownum,colnum)]
		wbxfNew = copyXF(wbOld,wbxfOld)
		shNew.col(colnum).width = shOld.colinfo_map[colnum].width
		shNew.write(rownum,colnum,rowOld[colnum],wbxfNew)
wbNew.save("switch-1st.xls")

	


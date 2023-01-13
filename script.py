import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

codEntidade = cfg['DEFAULT']['CodEntidade']
nomeEntidade = cfg['DEFAULT']['NomeEntidade']

scripts = {
'nota' : f""" select
n.cdautenticacao,
n.nrnfs,
replace(n.dtemissaonfs,',','.') as dtemissao,
n.vltotalnota,
n.vltotaldeducoes,
n.vlcofins,
n.vlcsll,
n.vlinss,
n.vlirpj,
n.vlpis,
TRIM(REPLACE(REPLACE(n.dscomentario,CHR(10),' '), CHR(13),' ')) as comentario,
n.tptributacao,
n.isissretido,
n.vlimposto,
n.isnotacancelada,
n.tpopcaosimplesnfs,
n.vlaliquotacofins,
n.vlaliquotacsll,
n.vlaliquotainss,
n.vlaliquotairpj,
n.vlaliquotapis,
n.iscartacorrecao,
n.tpdocumentofiscal,
n.idcidadeprestacaoservico, --Id
TRIM(REPLACE(REPLACE(n.dsimpostos,CHR(10),' '), CHR(13),' ')) as dsimpostos,
n.vldesconto,
ns.idservicoaesubitem, --Id
TRIM(REPLACE(REPLACE(ns.dsdiscriminacaoservico,CHR(10),' '), CHR(13),' ')) as dsdiscriminacaoservico,
ns.vlservico,
ns.vlaliquota,
ns.vldeducao,
TRIM(REPLACE(REPLACE(ns.dsjustificativadeducao,CHR(10),' '), CHR(13),' ')) as dsjustificativadeducao,
p.nmpessoa as prestador,
p.nrinscricaomunicipal as inscricaomunicipal,
p.nrinscricaoestadual as inscricaoestadual,
p.nmfantasia as nomefantasia,
p.nrdocumento as documentoprestador,
p.nrcep as cep,
p.dsendereco as endereco,
p.nrendereco as nrendereco,
p.dscomplemento as complemento,
p.nmbairro as bairro,
p.nmcidade as cidade,
p.nrtelefone as telefone,
p.dsemail as email,
p.dtenquadramentosimples as enquadramentosimples,
p.tpissnfs as tipoiss,
p.issubstitutotributario as substitutotributario,
p.tpopcaomeinfs as mei,
p.idcidade as idcidadeprestador, -- id
pt.nmpessoa as tomador,
pt.nrinscricaomunicipal as inscricaomunicipaltomador,
pt.nrinscricaoestadual as inscricaoestadualtomador,
pt.nrdocumento as documentotomador,
pt.nrcep as ceptomador,
pt.dsendereco as enderecotomador,
pt.nrendereco as nrenderecotomador,
pt.dscomplemento as complementotomador,
pt.nmbairro as bairrotomador,
pt.nmcidade as cidadetomador,
pt.nrtelefone as telefonetomador,
pt.dsemail as emailtomador,
pt.idcidade as idcidadetomador -- id
from nfs_nota n
join nfs_notadetalhe nd on nd.idnfs = n.idnfs
join nfs_pessoa p on (p.idpessoa = n.idpessoaprestador)
join nfs_notaservico ns on (ns.idnfs = nd.idnfs)
left join nfs_pessoa pt on (pt.idpessoa = n.idpessoatomador)
where p.identidade = {codEntidade}
order by n.idnfs, n.dtemissaonfs
 """,

'cidades' : f""" select
c.idcidade as id,
c.nmcidade as nome,
c.nmuf as uf,
c.cdibge as ibge
from nfs_cidade c """,

'subitem' : f"""
select
ss.idservicoaesubitem,
ss.nrservicoaesubitem,
ss.dsservicoaesubitem,
ss.idservicoaeitem
from nfs_servicoaesubitem ss
where identidade = {codEntidade} """,

'item' : f"""
select
si.idservicoaeitem as iditemservico,
si.nrservicoaeitem as nritemservico,
si.dsservicoaeitem as dsservico
from nfs_servicoaeitem si
where identidade = {codEntidade} """,

'notas_canceladas' : f"""
select
p.nrdocumento as prestador,
n.nrnfs as nrNfs,
n.tpdocumentofiscal as tpdocumentoFiscal,
nc.dtcancelamento as datacancelamento,
nc.dscancelamento as descricao
from nfs_notacancelamento nc
join nfs_nota n on (n.idnfs = nc.idnfs)
join nfs_pessoa p on (p.idpessoa = n.idpessoaprestador)
where p.identidade = {codEntidade} """,

}
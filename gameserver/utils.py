from typing import Coroutine, List
from uuid import UUID
from passlib.context import CryptContext
from random import SystemRandom
import asyncio
import bcrypt
import namemaker
import config as configuration

config = configuration.get_config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


_a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
__a = "abcdefghijklmnopqrstuvwxyz"


def gen_key(seed:int, size: int) -> str:
    global _a
    r = SystemRandom(seed)
    l = len(_a) - 1
    a = "{:016x}.".format(seed)
    for _ in range(size):
        v = _a[r.randint(0, l)]
        a = f"{a}{v}"
    return a


def roll_dice(d20: str) -> int:
    (n, m) = d20.lower().split("d", 1)
    s = m
    if not m.isnumeric():
        if "+" in m:
            (s, m) = m.split("+")
            m = int(m)
        if "-" in m:
            (s, m) = m.split("-")
            m = -(int(m))
    r = SystemRandom()
    v = 0
    for _ in range(n):
        v += r.randint(1, int(s))
    v += m
    return v


def json_converter(o):
    if isinstance(o, UUID):
        return o.hex


async def gen_system_names(num) -> List[str]:
    nameset = "andromeda antlia apus aquarius aquila ara aries auriga bootes caelum camelopardalis cancer canesvenatici canismajor canisminor capricornus carina cassiopeia centaurus cepheus cetus chamaeleon circinus columba coma corona corvus crater crux cygnus delphinus dorado draco equuleus eridanus fornax gemini grus hercules horologium hydra hydrus indus lacerta leo leominor lepus libra lupus lynx lyra mensa microscopium monoceros musca norma octans ophiuchus orion pavo pegasus perseus phoenix pictor pisces puppis pyxis reticulum sagitta sagittarius scorpius sculptor scutum serpens sextans taurus telescopium triangulum tucana ursamajor ursaminor vela virgo volans vulpeculaacamar achernar achird acrab acrux acubens adhafera adhara ain aladfar alamak alathfar alaraph albaldah albali albireo alchiba alcor alcyone aldebaran alderamin aldhafera aldhibah aldib alfirk algedi algenib algenib algieba algol algorab alhajoth alhena alioth alkaid alkalurops alkes alkurah almach alnasl alnilam alnitak alniyat alphard alphecca alpheratz alrai alrakis alrami alrischa alsafi alsciaukat alshain alshat altair altais altarf alterf aludra alwaid alya alzir ancha angetenar ankaa antares arcturus arich arided arkab armus arneb arrakis ascella asellus ashlesha askella aspidiske asterion asterope atik atlas atria auva avior azaleh azelfafage azha azimech azmidiske baham baten becrux beid bellatrix benetnasch betelgeuse botein brachium canopus capella caph caphir castor castula celbalrai celaeno chara chara cheleb chertan coxa caiam cursa cynosura dabih decrux deneb denebola dheneb diadem diphda dnoces dschubba dubhe duhr edasich electra elmuthalleth elnath eltanin enif errai etamin fomalhaut furud gacrux gatria gemma gianfar giedi giennah girtab gomeisa gorgonea graffias grafias grassias grumium hadar hadir haedus haldus hamal hassaleh hydrus heka heze hoedus homam hyadum hydrobius izar jabbah jih kabdhilinan kaffaljidhma kajam kastra keid kitalpha kleeia kochab kornephoros kraz ksora kuma lesath maasym mahasim maia marfark marfik markab matar mebsuta media megrez meissa mekbuda menchib menkab menkalinan menkar menkent menkib merak merga merope mesarthim miaplacidus mimosa minchir minelava minkar mintaka mira mirach miram mirfak mirzam misam mizar mothallah muliphein muphrid murzim naos nash nashira navi nekkar nembus neshmet nihal nunki nusakan okul peacock phact phad pherkad pherkard pleione pollux porrima praecipua procyon propus proximacentauri pulcherrim rana rasalas rastaban regor regulus rigel rotanev ruchba ruchbah rukbat sabik sadachbia sadalbari sadalmelik sadalsuud sadatoni sadira sadr sadlamulk saiph saiph salm sargas sarin sceptrum scheat scheddi schedar segin seginus sham shaula sheliak sheratan sinistra sirius situla skat spica sterope sualocin subra suhail suhel sulafat sol syrma tabit tarazet taygeta terebellum thabit theemin unukalhai vega vindemiatrix wasat wei wezen wezn yildun zaniah zaurak zavijava zedaron zelphah zibal zosma zubenelgenubi zubenelgubi zubeneschemali zubenhakrabi Acestes Achilles Acis Acontius Actaeon Admetus Adonis Aeacus Aedon Aeolus Aethra Agamemnon Aglauros Alcestis Alcithoe Alcmaeon Aloadae Amalthaea Amazon Amphion Amphitrite Amphitryon Ananke Ancaeus Anchises Andromache Andromeda Anius Antaeus Antilochus Antiope Aphrodite Apollo Ares Arethusa Argonaut Argus Ariadne Aristaeus Artemis Asclepius Astyanax Atalanta Athamas Athena Atlas Augeas Autolycus Baucis Bellerophon Bendis Biton Boreas Briareus Britomartis Busiris Cabeiri Cadmus Caeneus Calais Calchas Calliope Callisto Cassandra Castalia Cecrops Centaur Cephalus Chaos Charon Chimera Chiron Circe Cleobis Clio Clytemnestra Cotys Cronus Cyclops Cyrene Daedalus Danaus Daphne Daphnis Dardanus Demeter Demophon Deucalion Diomedes Dione Dionysus Dioscuri Echidna Echo Eileithyia Electra Elysium Endymion Eos Erato Erechtheus Erigone Eris Eros Eumolpus Europa Eurydice Euterpe Evander Fama Fate Furies Gaea Galatea Galinthias Ganymede Glaucus Gorgon Grace Hades Harmonia Harpy Hebe Hecate Hector Hecuba Helen Helenus Helios Hellen Hephaestus Hera Heracles Hermaphroditus Hermes Hero Hesperides Hesperus Hestia Hippolytus Hora Hyacinthus Hyades Hydra Hygieia Hylas Hymen Hyperborean Hypnos Hypsipyle Iacchus Iasion Icarus Idomeneus Ilos Io Iolaus Iphigeneia Iris Ixion Jason Laestrygones Lamia Laocoon Laomedon Leander Leda Lethe Leto Leucothea Linus Lotus-Eater Lucifer Lycaon Manto Marsyas Medea Medusa Melampus Meleager Melpomene Memnon Menelaus Midas Minos Minotaur Mnemosyne Morpheus Muse Myrmidon Naiad Narcissus Nemesis Neoptolemus Nereid Nereus Nestor Nike Ninus Niobe Nisus Nyx Oceanus Odysseus Oedipus Oenone Orestes Orion Orpheus Pan Pandarus Pandora Paris Pegasus Peleus Pelias Pelops Penelope Persephone Perseus Phaethon Philemon Philoctetes Phocus Phoebe Phoenix Pirithous Pleiades Plutus Polymnia Polyphemus Polyxena Poseidon Priam Priapus Procrustes Proetus Prometheus Protesilaus Proteus Psyche Pygmalion Python Rhea Sarpedon Satyr Selene Semele Serapis Silenus Siren Sisyphus Styx Tantalus Tartarus Telegonus Telemachus Tereus Terpsichore Thalia Thamyris Thanatos Themis Theseus Thetis Tiresias Titan Tithonus Triton Troilus Tyche Typhon Urania Uranus Zetes Zethus Zeus"
    ns = namemaker.make_name_set(
        nameset.split(" "), order=2, name_len_func=len, clean_up=True
    )
    n = set()
    while len(n) <= num - (num / 3):
        c = ns.make_name(
            exclude_history=True, exclude_real_names=True, add_to_history=True
        ).capitalize()
        if badword(c):
            continue
        print(f"{c}")
        n.add(str(c))
        await asyncio.sleep(0.0001)
    while len(n) < num:
        r = SystemRandom()
        s = ""
        while len(s) < 3:
            a = __a[r.randint(0, len(__a) - 1)]
            s = f"{s}{a}"
        d = r.randint(1, 999)
        s = "{:s}-{:03d}".format(s, d).upper()
        print(f"{s}")
        n.add(s)
        await asyncio.sleep(0.0001)
    ret = list(n)
    ret.sort()
    return ret

def badword(c: str) -> bool:
    if c.strip().lower() in ["penis", "ass", "fuck", "shit", "bitch", "cunt", "dick", "pussy", "vagina", "boob", "boobs", "breasts", "dick", "nutsack"]:
        return True
    return False

def wait(fn: Coroutine):
    event_loop = asyncio.get_event_loop()
    if event_loop is None:
        event_loop = asyncio.new_event_loop()
    return event_loop.run_until_complete(fn)
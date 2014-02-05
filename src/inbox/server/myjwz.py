#!/usr/bin/python

from jwzmessage import JWZ_Message
import jwzthreading

# THREAD (1)
MSG1 = """From Kavya Joshi Mon Feb  3 12:45:50 2014
X-Apparently-To: inboxapptest@yahoo.com via 72.30.237.74; Mon, 03 Feb 2014 20:45:52 +0000
Return-Path: <kavya@inboxapp.com>
X-YahooFilteredBulk: 209.85.217.171
Received-SPF: pass (domain of inboxapp.com designates 209.85.217.171 as permitted sender)
X-YMailISG: TpDMoi0WLDsTi1ki35nDmkZr2xCA.PA2NkI2fLTnDIAauB9.
 0AzskfNBjDDqdfm3JBQSEgzetdLKzwmhsnJDhlmHUiN5maCOsdqLqzo51hAx
 RfRIwSdlFqHBl_VGbi28_54h8HLwSRk7CH61wpWYuHuITq6qjNUX0sS6IvvE
 MwJWBO20LB3vSXq9QK7QJDI3RaH0cY5BolC4AGzPyMR56vM5CNcbWV2D9yDY
 rbDi5BAsVR0Xr.D2pagxHr8DmdMKMda1drgyjIcvW1Vlk0OSV31Dh7tpikUB
 kUEdwz_lTDkiQDSa46x3EOVKY4lnX80piFuAMY1TODDWYAroPm_QxeniHMJm
 .17rfuNSRKTvFwIDVivdjgfjM4hBAqKQLmM9nhWgYCYHZ3tbqNtKyxQ1H8Q_
 NC7PMi0DJgNxe2vq3Qtk0OrA6QeeRCQcc070e77Po_irPizvwZmSnB5GXdDe
 c6Yk0nYVJVrGQxUll9Z8VuWCDvALUDKsFV.veZpDoAfR9KcPAGQQuRRSIDJ4
 EmtorTKDd8nTtvU0BNT0nFu6iyV0EgB_UCG9Ekh4QC0soZjQbX9WmldY7HNy
 eR6aUsTUho._LS.xGpgYSlP7tHDQpyVsmPp0GtJEIf6vhoprLf198Z2hLWle
 jJ70TRzpVF.GAovtYgzv5fz6Hu2N_jUeIASzo5cCUTkZ0pLRbCybFJ6AmPwn
 bNai3sx3IzZv34cmhdHqjN17IUghCrinmsjco.wxU..XQgNPhIgbGE1jNwWT
 XMeO576kxuorhmO6WUNDrT8ycAiPRfePVVuT75Xhn6cCIFntBJ7fKWUp_ZYy
 CgzOmNzj.TdDcnq7YDQwhb5QXYZ2zw3asHceLQ3.eM2VnKFppA8u5uQ9oevE
 YCyXw6EDXGphuy0cBGUoV7yIyIFfRDoQscq8ynnn6Uj8ixylj46McaDJkfrV
 5Eev.hTM8EsfsYzbriQKs.H1YhLyAT.sZ_kCchVO1U.yTjmuy3gMdN_Cz4mx
 N3ZEN6r8fZMKFx6QcPnQl40S78rBr7YJerP2X7CUDPAx7X9U5gPlimcLat3G
 UpjBZirn1Gfu87ekNNzzIuDuKl4R3MV_F_7tu.lZ6Pxz6.ZT3KSMmdD1QExC
 uWyn.33liXhyfqGeJ.pqd_BM0UGEn7vur3hENLwnEkCo33sHY3L6Pw9LrMCW
 2gSOTYW94dcsgP0cNXTnyWZWo9C.5Cki0v57vR09k4IOro0XR_HLuHSdEUCz
 cyOuN8HLqPEGKAyhZsJoNYvBOnrmCPFGPpil6Q7pdmHztwnLi92i_oE5sb.R
 p4s8QPHWQ3o5NBu9Vk_1Q2dlub78PMNTH3qicSpie6RaHUN9F433spdNo.Lf
 1Q--
X-Originating-IP: [209.85.217.171]
Authentication-Results: mta1380.mail.ne1.yahoo.com  from=inboxapp.com; domainkeys=neutral (no sig);  from=inboxapp.com; dkim=pass (ok)
Received: from 127.0.0.1  (EHLO mail-lb0-f171.google.com) (209.85.217.171)
  by mta1380.mail.ne1.yahoo.com with SMTPS; Mon, 03 Feb 2014 20:45:51 +0000
Received: by mail-lb0-f171.google.com with SMTP id c11so5767451lbj.16
        for <inboxapptest@yahoo.com>; Mon, 03 Feb 2014 12:45:50 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=inboxapp.com; s=google;
        h=mime-version:date:message-id:subject:from:to:content-type;
        bh=coGGcO/7Y29Ae+JWJan0T5Dc67Q3rEA9tU96I4sggIA=;
        b=kubcdo1c4v/qnW872esi7fzGZ8OTL1xIqXO5qSM+R+tyb1L3yBYVVu5Cxk3shyJkHF
         jq7EviLz+0bInjeqG4HOseYMhUpqULGjFNzN2o8AllFCNI1b2dc3z30FW1QyycXggr/I
         cXlJtfvTBGIsyu9uTmxGHES7FuoqfrjP5Ngiw=
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20130820;
        h=x-gm-message-state:mime-version:date:message-id:subject:from:to
         :content-type;
        bh=coGGcO/7Y29Ae+JWJan0T5Dc67Q3rEA9tU96I4sggIA=;
        b=Tx4bM2IhgIrjGGXVeSxaaTLdEQ3ICGg1s/dovXG8YADMpEbcnuf6O6LUtKvhEAGSb3
         rBWFhcivcfNZj9M+YYpIOenASfRzUdeIpcsrSoIS54rV/a2hd0ThWJw2IWIu0bNdLfOg
         9V6z1ar3lP5PUYEo0zuUYRK6E9pk+LBJxcwaU+gtn4d0Tuv7aJW5MTP61yF6HAcYvJai
         HDQ0985IOm6V3SZffqalfVGZtuZAUlRJzXtkYCdeaB5t+bx2JumE/L/rtjzJxEWetLyO
         nJ1vvLyYHAGVNYL4V/Kyd9a8Ja25iL+O6y/kSv3wcmC22C39iV21eISgRRnD2sLtLXH/
         YcbA==
X-Gm-Message-State: ALoCoQkE3Lyx94ZP1zINUPniG3/2MP+I6t4WcOdXohs1BSxXQc8pRnM3Fp3mcnEX5ZHf6Zt4s0eg
MIME-Version: 1.0
X-Received: by 10.112.43.70 with SMTP id u6mr13901395lbl.30.1391460350664;
 Mon, 03 Feb 2014 12:45:50 -0800 (PST)
Received: by 10.112.225.236 with HTTP; Mon, 3 Feb 2014 12:45:50 -0800 (PST)
Date: Mon, 3 Feb 2014 12:45:50 -0800
Message-ID: <CALkxmqBeix8Gia3po6yemjRCe8viAkp4+O7KFHbfCvUULpHngQ@mail.gmail.com>
Subject: Test Conversations
From: Kavya Joshi <kavya@inboxapp.com>
To: Inbox App <inboxapptest@yahoo.com>
Content-Type: multipart/alternative; boundary=001a1135e0f4ebb9f304f1869b2a
Content-Length: 215

--001a1135e0f4ebb9f304f1869b2a
Content-Type: text/plain; charset=us-ascii

Hello, *Alice*

--001a1135e0f4ebb9f304f1869b2a
Content-Type: text/html; charset=us-ascii

<p>Hello, <b>Alice</b></p>

--001a1135e0f4ebb9f304f1869b2a--
"""

# NOT THREAD
msg2 = """From Kavya Joshi Mon Feb  3 12:53:22 2014
X-Apparently-To: inboxapptest@yahoo.com via 72.30.237.73; Mon, 03 Feb 2014 20:53:23 +0000
Return-Path: <kavya@inboxapp.com>
X-YahooFilteredBulk: 209.85.217.181
Received-SPF: pass (domain of inboxapp.com designates 209.85.217.181 as permitted sender)
X-YMailISG: TtbFz9QWLDsIKenB1Q6Vbw8GCSlHEbrfj_XR1ICEvht9cgq2
 pSIMdyCqXV2XuHAooBg0PrJT2R2O15eanrjlWybD.CfEa78AQQGJb7V3sqyl
 58UeFVerZSUfkZS8Qq2hfdniHWHCTWWP1H.J4_rQtNT_u9lSRlJJ2n4Uy4i.
 Wlf8sRw1lMrhGuQI8ru1y8CMG6gsqSLKhluVKMb_8m_1LPdfRkKbQzqMrHLM
 oTyTSXDQpKoSKyXONAvUISLfVFu4cnkyVf68HALp6vJWS9TNuzU22P2CgA1Y
 bF24U1NOxK4dcqlu68n5f5OdJ3DHzu8pY7.CUyo6nCtGSi4pNdLHbLQ05U7y
 O4aCUMyLNFQ6P5ai2TV4HezpcIXkM7DLguzZVNlBL2WhHTk9uojST5TwQNZ1
 u_5r2syyvbmPdLiUbpIEWZinlsgjlsuYcFi6PleStPrZKEReIEQYgACbJjbn
 0PB2gCnR71gZ.ZYm.aj1wW9oMvEwLNKt.9plO4YjxuspuPZ8ND7MI26_YJGl
 w06iQaKNA6IWWuenEtdp1nvwM9il3rW6IF0N8nsfmYgD8RMO1Aw0lf8ktk0z
 eejgMekKa6JJ_croQ533GCWbDMTThqM8xnDRoE8myMJzla01_VvA1QlRC2se
 Je_IiHRj6TmvTcHm9XxELvWGpRWPR_m00vcSVOLHyCY.tw_9L8hFmKuVzTgb
 ywfPJN0Vq6CJYr1D6oQuz7iF7izodXeBXMH2YEqICujNa3bRMU130x4.W6iS
 IS3K8YYBEngKYtYY0KxCudj_hfWi9UZfNepBWgJDkxH5k2Wrjc.D170PXe.m
 WAEbi8NOoZNmEzUE2anWySkv1H4rO1LvZ9ZLZ7Esrp8GnhMiTGeWHX71x15A
 H.Aok5HuP.EzNRSbqYbEQ.d8WqY38tWe8cXtnsK6ZF0dmDdefLXkanGzXzd4
 _r0SlrtdIOLi9E6kRS9VvH_RjKQgkNT7xEcyCLpV3WIGGuzK7ytWs07fLQRR
 tCMN661OJmSbhjrNbNYC.MKL0cNAfMDr7RlDB6W0b.WaYdeljBpZv.Lig8ZQ
 VYM0YC2eRpvWwfreLwS_pwFH_HvRHb0w5PnMeznCjsenWfCS_OeGheKm2oGM
 z5V0AnJqkp0n9pgIJ5sCQ_b35VUkAJyOx6QWi2kg9ic6FXR4yBmkyp2ByI0p
 YXEfWoTs2IWpxvj7Lv_J6tkvNs3l9Fm67wsREQTJPRXUqXxKfdnSbFlml8hO
 z0Poos3kLOMn.fxXm.LFVcZFzutMxwfmaGRDFxm7d8mzPrHMaYAzESXd76BW
 eUmNdprJ8kPRQEOnDTJGAiDxhwH5URh8YS9h6CA3djJo86DLBMlzqb5rQ6b6
 jbymeh8-
X-Originating-IP: [209.85.217.181]
Authentication-Results: mta1099.mail.ne1.yahoo.com  from=inboxapp.com; domainkeys=neutral (no sig);  from=inboxapp.com; dkim=pass (ok)
Received: from 127.0.0.1  (EHLO mail-lb0-f181.google.com) (209.85.217.181)
  by mta1099.mail.ne1.yahoo.com with SMTPS; Mon, 03 Feb 2014 20:53:23 +0000
Received: by mail-lb0-f181.google.com with SMTP id z5so5687336lbh.40
        for <inboxapptest@yahoo.com>; Mon, 03 Feb 2014 12:53:22 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=inboxapp.com; s=google;
        h=mime-version:date:message-id:subject:from:to:content-type;
        bh=1xB8QOUBc8SVB67caYUUN5IhUmvrTLg5aVvJoSbMi48=;
        b=0kEsL2Gj/9EayIDOiP3HZE3JlNuLuT6FZRvSZEXdvr46KEYeRoFKCsnO4o3Oyk3VB5
         xNRddV//Cgi75mtjj4ShgkBPKEJwt8tSqBwWcyB2q6GnVS+bkEKcUb5/wGU2pb4Zvab2
         EVET93hdQ1QCzONDLWo6cFNa0d6Mq/eoQAGMc=
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20130820;
        h=x-gm-message-state:mime-version:date:message-id:subject:from:to
         :content-type;
        bh=1xB8QOUBc8SVB67caYUUN5IhUmvrTLg5aVvJoSbMi48=;
        b=YqRyedYKox9AfO4oBGuv2OYC0yyJtNUndsNYdgsQ7QqQhlz8aatIVnF8k7sBWUq9tr
         HdR9nzIq8avzVEjy42u3GREG2Mkp4ffj7ixrkoV7ifwlJQa0/rveLNDkaeSTVIXJgHTN
         OHC3EXrK9sYHJcFvrPNrxBNRt5JN3SBAujiZ8ELksDImdSiRWdklVr6aKN8BigEaf2jt
         F6ZWTGa6qDObkRw5Asx99Ey2nG6u5iQwKEQqbZaOWkag429H8jjtjzUP/NxqEIiPRx+6
         2Idq3V090kLWLYYBZehlqkHaWiAN/iEaBAwIfGm6U+HmaKQVdwdzNv7d1BxRBmsNbLOm
         S3fw==
X-Gm-Message-State: ALoCoQmBDU8QFPazOHtIzZs+ha5J7mzc9YBfeo6C4bJBbN/Z6Ry5G0jWocPip4bheAk8DNz6UBIY
MIME-Version: 1.0
X-Received: by 10.152.8.47 with SMTP id o15mr14954154laa.20.1391460802287;
 Mon, 03 Feb 2014 12:53:22 -0800 (PST)
Received: by 10.112.225.236 with HTTP; Mon, 3 Feb 2014 12:53:22 -0800 (PST)
Date: Mon, 3 Feb 2014 12:53:22 -0800
Message-ID: <CALkxmqDUWw4uzir=PkMdtRY_6Y8Bzn_cppJ_uS0Th6W8jTMePw@mail.gmail.com>
Subject: Test Conversations
From: Kavya Joshi <kavya@inboxapp.com>
To: Inbox App <inboxapptest@yahoo.com>
Content-Type: multipart/alternative; boundary=001a11c36402d7048d04f186b69f
Content-Length: 219

--001a11c36402d7048d04f186b69f
Content-Type: text/plain; charset=us-ascii

Hello, *Alice*

--001a11c36402d7048d04f186b69f
Content-Type: text/html; charset=us-ascii

<p>Hello, <b>Alice</b></p>

--001a11c36402d7048d04f186b69f--
"""

# THREAD (2)
msg3 = """From Inbox App Mon Feb  3 12:46:17 2014
X-YMail-OSG: tOeFpAUVM1lppssn0lSsALdEVQZLS5.6e11qxOoPWl2JpOl
 cIldZ8wHuIbyfMmN6hkpDysEdq_ac53K2GcT0tB5AOgV87RW2qzd_AHy8NQA
 6FpK_xR76AhrqChtoq6p2O1ndG0ixrBkkkOpuKNnua_3dQ_yrIi9xEl8rUhc
 Xhqp47gpOxCwC5JeTjYfrCpv4Tjej6reXrzRly99E83uD43i4z2tXa7P3jqR
 2Ymkh.j2abHk39cB0g0EiJwyqgATH3DoT8R3PDtg1JID0vMO_kkIHnlAwjRk
 klDfwGkWBKS9GL3N1V6b6v.KIYBiYKWonDi7r_1s5I4KUKLuiOdX7c6LA1sw
 mIbRMeaXR1CyMTiucXuzSxbHtjoZd6BxGMI9UXLZiGHyrGROjNquPrTnzHuI
 eZuX8ZTNLVLmR40wcP1bL4d3F4BfLWngIRPYennn2PDE.2NUIVvJvm0BGrLl
 I1XcfhF4PJpWLHzq8hGhnCPS6FI8FGn3cFEwTH5TJ4Usk785TSBlneP4f1HX
 9uwNkBIVg0RlS_07278DXpMU-
Received: from [173.13.150.22] by web162804.mail.bf1.yahoo.com via HTTP; Mon, 03 Feb 2014 12:46:17 PST
X-Mailer: YahooMailWebService/0.8.174.629
References: <CALkxmqBeix8Gia3po6yemjRCe8viAkp4+O7KFHbfCvUULpHngQ@mail.gmail.com>
Message-ID: <1391460377.71983.YahooMailNeo@web162804.mail.bf1.yahoo.com>
Date: Mon, 3 Feb 2014 12:46:17 -0800 (PST)
From: Inbox App <inboxapptest@yahoo.com>
Reply-To: Inbox App <inboxapptest@yahoo.com>
Subject: Re: Test Conversations
To: Kavya Joshi <kavya@inboxapp.com>
In-Reply-To: <CALkxmqBeix8Gia3po6yemjRCe8viAkp4+O7KFHbfCvUULpHngQ@mail.gmail.com>
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="-1621810148-1897437080-1391460377=:71983"
Content-Length: 1089

---1621810148-1897437080-1391460377=:71983
Content-Type: text/plain; charset=us-ascii

Hello, *Alice*

---1621810148-1897437080-1391460377=:71983
Content-Type: text/html; charset=us-ascii

<p>Hello, <b>Alice</b></p>

---1621810148-1897437080-1391460377=:71983--
"""

# THREAD (3)
msg4 = """From Kavya Joshi Mon Feb  3 12:50:15 2014
X-Apparently-To: inboxapptest@yahoo.com via 72.30.237.73; Mon, 03 Feb 2014 12:50:20 -0800
Return-Path: <kavya@inboxapp.com>
X-YahooFilteredBulk: 209.85.215.48
Received-SPF: pass (domain of inboxapp.com designates 209.85.215.48 as permitted sender)
X-YMailISG: bYhpD4gWLDuFlSt7ErbGEUf8w050LAsiHOeFTSKnsUFmg1UC
 cBNbDi5OhVsjMUbWiKGaIruSxDBxnT0KWOzew4vwYYcprMSf700MZu9JkZjA
 fozR2lGPi8zpAM7aX0zf4nuQFKIJvcqJQrafhhQxdGY3fEnhUzw8J9lTxW7C
 mgkX_T5dI6fwbq_CfcXnSEho70pFVBp.hfHGJz6YXRU5zl.CTLkDQn6gS8oH
 PK2fr4qW56Q8pst1tz7C3V7qS.qs.pZFLv1SpKKpvIWEYUjOuH8qwXzyujcR
 Ljx1s1rtsu_LAYAV3q.tIbae8MY5hJDyK6i4Y6Q0Q8ScMcweM5fuXNyIXshd
 ayERDnkiW3cpuZFhYgGOwO4dLK63QFLpwcgzEyfsjNJufwmiUx5MOZHweGWw
 5Xj9pXd4A709_tnhbcFncferZ4rcw8q44_8CbCMQownnLRksHL8Ktmlmfti5
 wLoP.5aCL4pFTs4gAEylmuPp.EgbpRjPhpgvXu3663LDPYm._OEpQ.bK9O3W
 M17v5gtAZPdV3PZzlt5Z17eIZ.NznFRH0WNZOXWMe01xRQ43HwUmkCqMdyxx
 p1I7Fy._nIuv5KayY2DxtG3XeSvLYo7EGmBDxNhLI4E1Z9UxtOttUoXOhrGy
 raMuZ_J1cD1eogarEGZ0lQIOGg_jL.UPP5RoV5Ml215_i0vaIQYuk8.rwClW
 Sp0G5paGjzjMlk8gk8eBmLN982T1v6jzD4is4wPUjiyPKbZMqzEKiegGgWC2
 Ia4SuPROCBWiN8BvjBzhxs_dauzZf12eDR0p5nw2mfpiOeCOLqVQLw20C.iX
 BLOCQS6OWbtuETTae3n0Dwd9qDr1OuD2_X69BEBRHzgKDrZwz7JKSplGvtjv
 10B_hTSSuUIVcZXsEOZ0Sjm7imz9q45aL3zu4gfMMbYBx_oe8qZ8zqwPHmsf
 3RWACrp_9rmpTZE.4epmh2RqN9TOlPyEAAz0XWnd1PIRW.m3Z2hd6CElBfnN
 yI2mB_RhfcHX8D_tUvqfZTkA.a9Z.geujz30kLpaJGiba0lkNrg4kYmoKfqV
 kMUnPMksj3amlzQvdQ9biFhSAHbx7HoDG.YmSTq9C20TEwvYDgbzYayoLoZq
 oqJ_DA00GxuKWfjYjJEkcwLCfyt98DHdsE5jWRtZibi2L.YD6o5_GJxbeKl.
 yXQcF.YADR0434pPmkHoCeCpgHo66CSiQE0Yd0k83SaOse_dNUq6YTwQnZoP
 Id6r_rwJ.8aBPwoz0PYh6RvVbsshCLkyGaKrkVcoT09Qg4ek_vccf2c21lpE
 BEnR2tP.hOqiqYwL0LX6P7ly.xcp5z2TeaQCNkYJ0yx.VI.lCXIAQcyTOapf
 XQv9toojB5WbSwm8J3AQPac6jnPSjMkXj0K_lxJ9aVq0SoYdkZb02WQEBQ--
X-Originating-IP: [209.85.215.48]
Authentication-Results: mta1326.mail.gq1.yahoo.com  from=inboxapp.com; domainkeys=neutral (no sig);  from=inboxapp.com; dkim=pass (ok)
Received: from 127.0.0.1  (EHLO mail-la0-f48.google.com) (209.85.215.48)
  by mta1326.mail.gq1.yahoo.com with SMTPS; Mon, 03 Feb 2014 12:50:19 -0800
Received: by mail-la0-f48.google.com with SMTP id mc6so5836814lab.35
        for <inboxapptest@yahoo.com>; Mon, 03 Feb 2014 12:50:15 -0800 (PST)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=inboxapp.com; s=google;
        h=mime-version:in-reply-to:references:date:message-id:subject:from:to
         :content-type;
        bh=nODeMd3FRpyXiRYT0YIjIobPdtNFhVCmNoBOO6mAtJo=;
        b=L2ktA37KWVapgZ44Tii+zMzq8Z1i+/vE8vQEqxuLwEZNwkdG0Nkm0P8b7YEMmp1BaO
         c+CzTf/Dp11WTj7MHiVLy8CkPiaz16V3DJlethfYV/PU3O0A23I/y00XUTNUugsirpNh
         5R9HPvCkXQheORIZrzevx3TmfY90R6gZs77Yg=
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20130820;
        h=x-gm-message-state:mime-version:in-reply-to:references:date
         :message-id:subject:from:to:content-type;
        bh=nODeMd3FRpyXiRYT0YIjIobPdtNFhVCmNoBOO6mAtJo=;
        b=lYuah2wewuZl+YsBnuElBUhfoe+BZiCKZhnY1sJW5C8K+7gBVE+2rU20KWfaSI9Ci8
         l2GIf5TP+TY87hPboK3WFYV/TFE4e7QZq9Buw8TjoRbbrH1pSfUP+3PFuS6Lvw02AbTZ
         QdU47DV9zKPq6wZ3k9th3EQgnWtM2fTDKejQ+l4NZJTLWp6F688rRDIvXkkMy6hk6AG0
         27RVBo4b0LPk/bzrHyCI8T5synfbHGn6yrMvcWekJ7X6NXFdE2+rP8K7UtKbAlgBT4J1
         CGtEWjzbOJM7G5ebrboRMJXfPbdoyIvzhybN5yZZdle9f4aWZmfK5NTTr7MHXoClifRt
         F1CQ==
X-Gm-Message-State: ALoCoQlSdDSqZbL98NnG4UjZIiDyf6j4USyaGvwCl6Me+rQxs2QfkTwbV8rJ4P+EiJZJaOJBZoNH
MIME-Version: 1.0
X-Received: by 10.112.56.237 with SMTP id d13mr25632747lbq.2.1391460615339;
 Mon, 03 Feb 2014 12:50:15 -0800 (PST)
Received: by 10.112.225.236 with HTTP; Mon, 3 Feb 2014 12:50:15 -0800 (PST)
In-Reply-To: <1391460377.71983.YahooMailNeo@web162804.mail.bf1.yahoo.com>
References: <CALkxmqBeix8Gia3po6yemjRCe8viAkp4+O7KFHbfCvUULpHngQ@mail.gmail.com>
    <1391460377.71983.YahooMailNeo@web162804.mail.bf1.yahoo.com>
Date: Mon, 3 Feb 2014 12:50:15 -0800
Message-ID: <CALkxmqCOcAOVv=vRQkn8VRzGaCFRvaNY-ykQwdk0ssZoh=ifjw@mail.gmail.com>
Subject: Re: Test Conversations
From: Kavya Joshi <kavya@inboxapp.com>
To: Inbox App <inboxapptest@yahoo.com>
Content-Type: multipart/alternative; boundary=001a1133a922b256bc04f186ab70
Content-Length: 1579

--001a1133a922b256bc04f186ab70
Content-Type: text/plain; charset=us-ascii

Hello, *Alice*

--001a1133a922b256bc04f186ab70
Content-Type: text/html; charset=us-ascii

<p>Hello, <b>Alice</b></p>

--001a1133a922b256bc04f186ab70--
"""

msglist = []

# M1
jwz_msg1 = JWZ_Message(MSG1)
msglist.append(jwz_msg1)

# M2
jwz_msg2 = JWZ_Message(msg2)
msglist.append(jwz_msg2)

# M3
jwz_msg3 = JWZ_Message(msg3)
msglist.append(jwz_msg3)

# M4
jwz_msg4 = JWZ_Message(msg4)
msglist.append(jwz_msg4)

# Thread:
subject_table = jwzthreading.thread(msglist)
items = subject_table.items()

#print "items = ", items
#print "\n\n"
#for subj, container in items:
    #print "subj = ", subj
    #jwzthreading.print_container(container, debug=0)
